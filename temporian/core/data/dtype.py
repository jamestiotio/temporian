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

"""Data types declaration."""

import math
from enum import Enum
from typing import Union


class DType(Enum):
    """The type of a feature."""

    FLOAT64 = "float64"
    FLOAT32 = "float32"
    INT64 = "int64"
    INT32 = "int32"
    STRING = "str_"
    BOOLEAN = "bool_"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value

    @property
    def is_float(self) -> bool:
        return self in (DType.FLOAT64, DType.FLOAT32)

    @property
    def is_integer(self) -> bool:
        return self in (DType.INT64, DType.INT32)

    def missing_value(self) -> Union[float, int, str]:
        """
        Returns missing value for specific dtype.

        Returns:
            The default missing value for the given data type.
        """

        if self.is_float:
            return math.nan

        if self.is_integer:
            return 0

        if self == DType.STRING:
            return ""

        raise ValueError(f"Non-implemented type {self}")

    @classmethod
    def from_python_type(cls, python_type: type) -> "DType":
        """
        Returns DType from python type.

        Args:
            python_type: Python type.

        Returns:
            The corresponding DType.

        Raises:
            ValueError: If python_type is not implemented.
        """

        if python_type is float:
            return DType.FLOAT64

        if python_type is int:
            return DType.INT64

        if python_type is str:
            return DType.STRING

        if python_type is bool:
            return DType.BOOLEAN

        raise ValueError(f"Non-implemented type {python_type}")


# The dtype of indexes.

# TODO: IndexDType should only be the integer and str types in DType. Let's
# find a way for IndexDType to only represent those types.
IndexDType = DType


def check_is_valid_index_dtype(dtype: DType):
    if dtype not in [DType.INT32, DType.INT64, DType.STRING]:
        raise ValueError(
            f"Trying to create an index with dtype={dtype}. The dtype of an"
            " index can only be int32, int64 or string."
        )


# API dtypes definition

float32 = DType.FLOAT32
"""32-bit floating point number."""

float64 = DType.FLOAT64
"""64-bit floating point number."""

int32 = DType.INT32
"""32-bit integer."""

int64 = DType.INT64
"""64-bit integer."""

bool_ = DType.BOOLEAN
"""Boolean value."""

str_ = DType.STRING
"""String value."""
