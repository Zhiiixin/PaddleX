# copyright (c) 2024 PaddlePaddle Authors. All Rights Reserve.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import yaml

from ..ts_base.config import BaseTSConfig
from ....utils.misc import abspath


class TSAnomalyConfig(BaseTSConfig):
    """TS Anomaly Detection Config"""

    def update_input_len(self, seq_len: int):
        """
        upadte the input sequence length

        Args:
            seq_len (int): input length

        Raises:
            TypeError: if seq_len is not dict, raising TypeError
        """
        if "seq_len" not in self:
            raise RuntimeError(
                "Not able to update seq_len, because no seq_len config was found."
            )
        self.set_val("seq_len", seq_len)

    def update_dataset(self, dataset_dir: str, dataset_type: str = None):
        """
        upadte the dataset

        Args:
            dataset_dir (str): dataset root path
            dataset_type (str, optional): type to set for dataset. Default='TSDataset'
        """
        if dataset_type is None:
            dataset_type = "TSADDataset"
        dataset_dir = abspath(dataset_dir)
        ds_cfg = self._make_custom_dataset_config(dataset_dir)
        self.update(ds_cfg)

    def update_basic_info(self, info_params: dict):
        """
        update basic info including time_col, freq, target_cols.

        Args:
            info_params (dict): upadte basic info

        Raises:
            TypeError: if info_params is not dict, raising TypeError
        """
        if isinstance(info_params, dict):
            self.update({"info_params": info_params})
        else:
            raise TypeError("`info_params` must be a dict.")

    def _make_custom_dataset_config(self, dataset_root_path: str):
        """construct the dataset config that meets the format requirements

        Args:
            dataset_root_path (str): the root directory of dataset.

        Returns:
            dict: the dataset config.
        """
        ds_cfg = {
            "dataset": {
                "name": "TSADDataset",
                "dataset_root": dataset_root_path,
                "train_path": os.path.join(dataset_root_path, "train.csv"),
                "val_path": os.path.join(dataset_root_path, "val.csv"),
            },
        }

        return ds_cfg