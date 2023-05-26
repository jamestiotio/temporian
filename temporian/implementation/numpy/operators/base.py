import os
from abc import ABC, abstractmethod
from typing import Dict, Tuple

from temporian.core.data.node import Node
from temporian.core.operators.base import Operator
from temporian.core.operators.base import OperatorExceptionDecorator
from temporian.implementation.numpy.data.event_set import (
    EventSet,
    numpy_array_to_tp_dtype,
)


class OperatorImplementation(ABC):
    def __init__(self, operator: Operator):
        self._operator = operator
        # TODO: Check operator type

    @property
    def operator(self):
        return self._operator

    def call(self, **inputs: EventSet) -> Dict[str, EventSet]:
        """Like __call__, but with checks."""

        _check_input(inputs=inputs, operator=self.operator)
        outputs = self(**inputs)
        _check_output(inputs=inputs, outputs=outputs, operator=self.operator)
        return outputs

    @abstractmethod
    def __call__(self, **inputs: EventSet) -> Dict[str, EventSet]:
        """Applies the operator to its inputs."""


def _check_value_to_schema(
    values: Dict[str, EventSet],
    nodes: Dict[str, Node],
    label: str,
) -> None:
    """Checks if features are matching their definition."""

    for key, node in nodes.items():
        value = values[key]

        if value.schema != node.schema:
            raise RuntimeError(
                "Non matching schema between event set and input node. "
                f"event set={value.schema} vs "
                f"input node={node.schema}"
            )

        index_value = value.get_arbitrary_index_value()
        if index_value is not None:
            index_data = value.data[index_value]

            if len(index_data.features) != len(value.schema.features):
                raise RuntimeError(
                    f"Non matching number of {label} features. "
                    f"expected={len(value.schema.features)} vs "
                    f"effective={len(index_data.features)}"
                )

            for feature_value, feature_schema in zip(
                index_data.features, value.schema.features
            ):
                expecterd_tdtype = numpy_array_to_tp_dtype(
                    feature_schema.name, feature_value
                )
                if feature_schema.dtype != expecterd_tdtype:
                    raise RuntimeError(
                        f"Non matching {label} feature dtype. "
                        f"expected={expecterd_tdtype} vs "
                        f"effective={feature_schema.dtype}"
                    )

                if len(index_data.timestamps) != len(feature_value):
                    raise RuntimeError(
                        "Number of timstamps does not match number of feature"
                        " values"
                    )


def _check_input(
    inputs: Dict[str, EventSet],
    operator: Operator,
) -> None:
    """Checks if the input/output of an operator matches its definition."""

    with OperatorExceptionDecorator(operator):
        # Check input keys
        effective_input_keys = set(inputs.keys())
        expected_input_keys = set(operator.inputs.keys())
        if effective_input_keys != expected_input_keys:
            raise RuntimeError(
                "Input keys do not match the expected ones. "
                f"Received: {effective_input_keys}. "
                f"Expected: {expected_input_keys}."
            )

        _check_value_to_schema(inputs, nodes=operator.inputs, label="input")


def _check_output(
    inputs: Dict[str, EventSet],
    outputs: Dict[str, EventSet],
    operator: Operator,
) -> None:
    """Checks if the input/output of an operator matches its definition."""

    with OperatorExceptionDecorator(operator):
        # Check output keys
        effective_output_keys = set(outputs.keys())
        expected_output_keys = set(operator.outputs.keys())
        if effective_output_keys != expected_output_keys:
            raise RuntimeError(
                "Output keys do not match the expected ones. "
                f"Received: {effective_output_keys}. "
                f"Expected: {expected_output_keys}."
            )

        _check_value_to_schema(outputs, nodes=operator.outputs, label="outputs")

        for output_key, output_node in operator.outputs.items():
            output = outputs[output_key]

            # TODO: Check copy or referencing of feature data.
            matching_samplings = set(operator.list_matching_io_samplings())
            for input_key in operator.inputs.keys():
                input = inputs[input_key]

                expected_matching_sampling = (
                    input_key,
                    output_key,
                ) in matching_samplings
                is_same, reason = _is_same_sampling(output, input)
                if expected_matching_sampling and not is_same:
                    raise RuntimeError(
                        f"The sampling of input '{input_key}' and output "
                        f"'{output_key}' are expected to have THE SAME "
                        "sampling. However, a different sampling was generated "
                        f"during the op execution ({input} "
                        f"vs {output}). Reason: {reason}"
                    )


def _is_same_sampling(evset_1: EventSet, evset_2: EventSet) -> Tuple[bool, str]:
    if evset_1.schema.indexes != evset_2.schema.indexes:
        return (False, "Different index names")

    # Number of index values where to ensure that the numpy array containing
    # timestamps is the same for both evset_1 and evset_2.
    debug_mode = os.environ.get("TEMPORIAN_DEBUG_MODE", "0") in ["1", "true"]
    num_checks = 1 if debug_mode else len(evset_1.data)

    for i, (index_key, index_data_1) in enumerate(evset_1.data.items()):
        if i >= num_checks:
            break

        index_data_2 = evset_2[index_key]
        if index_data_1.timestamps is not index_data_2.timestamps:
            return (
                False,
                (
                    f"Timestamps at index key {index_key} are not the same"
                    " np.ndarray"
                ),
            )

    if debug_mode:
        # Compare index keys.
        # TODO: is there a way to avoid checking all keys here (keys might come in
        # different orders, can't compare top num_check keys in each evset)

        diff_keys = set(evset_1.data.keys()).difference(evset_2.data.keys())
        if diff_keys:
            return (
                False,
                f"Found {len(diff_keys)} different index keys",
            )

    return (True, "")
