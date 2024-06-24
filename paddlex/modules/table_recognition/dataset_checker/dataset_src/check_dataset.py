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
import json
import os.path as osp
from collections import defaultdict
from .....utils.errors import DatasetFileNotFoundError, CheckFailedError


def check(dataset_dir,
          output_dir,
          dataset_type="PubTabTableRecDataset",
          sample_num=10):
    """
    Check whether the dataset is valid.
    """

    if dataset_type == 'PubTabTableRecDataset':
        # Custom dataset
        if not osp.exists(dataset_dir) or not osp.isdir(dataset_dir):
            raise DatasetFileNotFoundError(file_path=dataset_dir)

        tags = ['train', 'val']
        max_recorded_sample_cnts = 50
        sample_cnts = dict()
        sample_paths = defaultdict(list)

        for tag in tags:
            file_list = osp.join(dataset_dir, f'{tag}.txt')
            if not osp.exists(file_list):
                if tag in ('train', 'val'):
                    # train and val file lists must exist
                    raise DatasetFileNotFoundError(
                        file_path=file_list,
                        solution=f"Ensure that both `train.txt` and `val.txt` exist in {dataset_dir}"
                    )
                else:
                    # tag == 'test'
                    continue
            else:
                with open(file_list, 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()
                    sample_cnts[tag] = len(all_lines)
                    for line in all_lines:
                        info = json.loads(line.strip("\n"))
                        file_name = info['filename']
                        cells = info['html']['cells'].copy()
                        structure = info['html']['structure']['tokens'].copy()

                        img_path = osp.join(dataset_dir, file_name)
                        if len(sample_paths[tag]) < max_recorded_sample_cnts:
                            sample_paths[tag].append(
                                os.path.relpath(img_path, output_dir))

                        if not os.path.exists(img_path):
                            raise DatasetFileNotFoundError(file_path=img_path)

                        boxes_num = len(cells)
                        tokens_num = sum([
                            structure.count(x)
                            for x in ['<td>', '<td', '<eb></eb>', '<td></td>']
                        ])
                        if boxes_num != tokens_num:
                            raise CheckFailedError(
                                f"The number of cells needs to be consistent with the number of tokens "\
                                "but the number of cells is {boxes_num}, and the number of tokens is {tokens_num}."
                            )
        meta = {}

        meta['train_samples'] = sample_cnts['train']
        meta['train_sample_paths'] = sample_paths['train'][:sample_num]

        meta['val_samples'] = sample_cnts['val']
        meta['val_sample_paths'] = sample_paths['val'][:sample_num]

        return meta