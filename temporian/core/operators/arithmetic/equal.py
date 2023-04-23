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

"""Arithmetic Equal Operator"""

from temporian.core import operator_lib
from temporian.core.data.dtype import DType
from temporian.core.data.event import Event
from temporian.core.data.feature import Feature
from temporian.core.operators.arithmetic.base import BaseArithmeticOperator


class EqualOperator(BaseArithmeticOperator):
    """
    Compares two Events element wise
    """

    @classmethod
    @property
    def operator_def_key(cls) -> str:
        return "EQUAL"

    @property
    def prefix(self) -> str:
        return "equal"

    # override parent dtype method
    def output_feature_dtype(
        self, feature_1: Feature, feature_2: Feature
    ) -> DType:
        return DType.BOOLEAN


operator_lib.register_operator(EqualOperator)


def equal(
    event_1: Event,
    event_2: Event,
) -> Event:
    """
    Compares two event features element wise

    Args:
        event_1: First event
        event_2: Second event

    Returns:
        Event: Event with features equal to the result of the comparison. True
            if the features are equal, False otherwise.
    """
    return EqualOperator(
        event_1=event_1,
        event_2=event_2,
    ).outputs["event"]
