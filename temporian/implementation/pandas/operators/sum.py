# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Implementation for the sum operator."""

from temporian.implementation.pandas.data.event import PandasEvent
from temporian.implementation.pandas.operators.base import PandasOperator

RESOLUTIONS = ["PER_FEATURE_IDX", "PER_FEATURE_NAME"]


class PandasSumOperator(PandasOperator):
    def __call__(
        self, event_1: PandasEvent, event_2: PandasEvent, resolution: str = None
    ) -> PandasEvent:
        """Sum two EventSequences.

        Args:
            event_1: First EventSequence.
            event_2: Second EventSequence.
            resolution: PER_FEATURE_IDX -> Sum is done to each feature index wise.
                        PER_FEATURE_NAME (Not implemented yet) -> Sum is done to each feature name wise.

        Returns:
            Sum of the two EventSequences.

        Raises:
            ValueError: If resolution is not one of PER_FEATURE_IDX or PER_FEATURE_NAME.
            ValueError: If event_1 and event_2 have different shape.
            NotImplementedError: If resolution is PER_FEATURE_NAME.
        """

        if resolution is not None and resolution not in RESOLUTIONS:
            raise ValueError(
                f"Resolution must be one of {RESOLUTIONS}, got {resolution}"
            )

        # raise value error if event_1 and event_2 have different shape
        if event_1.shape != event_2.shape:
            raise ValueError("event_1 and event_2 must have same shape.")

        # sum each feautre index wise
        if resolution is None or resolution == "PER_FEATURE_IDX":
            output = event_1.copy()
            for i, column in enumerate(event_1.columns):
                output.iloc[:, i] = event_1.iloc[:, i] + event_2.iloc[:, i]

        if resolution == "PER_FEATURE_NAME":
            raise NotImplementedError(
                "PER_FEATURE_NAME resolution not implemented yet."
            )

        output_feature_names = f"sum_{event_1.columns}_{event_2.columns}"
        output.columns = output_feature_names

        return {"output": output}
