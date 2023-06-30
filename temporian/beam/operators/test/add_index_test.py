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


from absl.testing import absltest

from temporian.implementation.numpy.data.io import event_set
from temporian.beam.test.utils import check_beam_implementation
from temporian.core.operators.add_index import add_index


class SelectTest(absltest.TestCase):
    def build_input(self, index_features=None):
        if index_features is None:
            index_features = ["a", "b"]
        return event_set(
            timestamps=[1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
            features={
                "a": ["x", "x", "x", "x", "x", "y", "y", "y", "y", "y"],
                "b": [1, 1, 1, 2, 2, 1, 1, 1, 1, 1],
                "c": [2, 3, 4, 3, 2, 22, 23, 24, 23, 22],
                "d": [100, 101, 102, 103, 104, 105, 106, 106, 107, 108],
                "e": [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10],
            },
            indexes=index_features,
        )

    def test_one(self):
        input_data = self.build_input(index_features=[])
        output_node = add_index(input_data.node(), "a")

        check_beam_implementation(
            self, input_data=input_data, output_node=output_node
        )

    def test_two(self):
        input_data = self.build_input(index_features=[])
        output_node = add_index(input_data.node(), ["a", "b"])

        check_beam_implementation(
            self, input_data=input_data, output_node=output_node
        )

    def test_on_top(self):
        input_data = self.build_input(index_features=["b"])
        output_node = add_index(input_data.node(), "a")

        check_beam_implementation(
            self, input_data=input_data, output_node=output_node
        )


if __name__ == "__main__":
    absltest.main()
