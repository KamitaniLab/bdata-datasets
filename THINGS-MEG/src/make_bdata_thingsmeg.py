from typing import Union

import os
from pathlib import Path
import csv

import bdpy
import numpy as np
import pandas as pd

import logging

import mne

import yaml
from typing import Dict, List, Optional, Union
from functools import partial
from glob import glob
from itertools import product
from pathlib import Path
import os
import hydra
from omegaconf import DictConfig, OmegaConf
import logging
import shutil

def make_bdata_thingsmeg(cfg: DictConfig, participant: str, preproc_data: mne.Epochs, output_dir: Path, logger: logging.Logger) -> None:
    """
    Make BData from preprocessed MEG data.
    
    :param cfg: Configuration.
    :param participant: Participant.
    :param preproc_data: Preprocessed MEG data.
    :param output_dir: Output directory.
    :param logger: Logger.
    
    """
    
    mode_list = ["exp", "test"] # exp is for training data, test is for test data
    
    for mode in mode_list:
        
        # get data
        feature_data, image_path_list = get_data(preproc_data, mode, cfg)
        
        # data reshape
        feature_data = feature_data.reshape(feature_data.shape[0], -1)
        
        # labels list
        label_list =[image_path.split('/')[-1].split(".")[0] for image_path in image_path_list]
        
        # labels index
        unique_labels = sorted(list(set(label_list)))
        image_index = [unique_labels.index(item)+1 for item in label_list]
        
        # vmap
        vmap = dict(zip(np.arange(len(unique_labels))+1, unique_labels))
        
        # add data
        brain_data = bdpy.BData()
        brain_data.add(feature_data, 'feature')
        brain_data.add(np.array(image_index).reshape(-1, 1).astype(int), "stimulus_name")
        brain_data.add_vmap("stimulus_name", vmap=vmap)
        
        # save
        mode_for_save = "train" if mode == "exp" else "test"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"sub-0{participant}_{mode_for_save}.h5")
        brain_data.save(output_file)
        logger.info(f"Saved {output_file}")


def get_data(preproc_data: mne.Epochs, mode: str, cfg: DictConfig) -> (np.ndarray, List[str]) :
    """
    Get data from preprocessed MEG data.
    
    :param preproc_data: Preprocessed MEG data.
    :param mode: Mode.
    :param cfg: Configuration.
    
    :return: Selected preprocessed data.
    """
    
    if cfg.category_overlap:
        feature_data = preproc_data[(preproc_data.metadata['trial_type']==mode)].get_data()
        image_path_list = preproc_data.metadata['image_path'][(preproc_data.metadata['trial_type']==mode)].to_list()
    else:
        train_categories = preproc_data.metadata['category_nr'][(preproc_data.metadata['trial_type']=='exp')].to_list()
        test_categories = preproc_data.metadata['category_nr'][(preproc_data.metadata['trial_type']=='test')].to_list()
        
        # remove overlap
        categories = {}
        categories['exp'] = list(set(train_categories) - set(test_categories))
        categories['test'] = test_categories
        
        feature_data = preproc_data[(preproc_data.metadata['category_nr'].isin(categories[mode]))].get_data()
        image_path_list = preproc_data.metadata['image_path'][(preproc_data.metadata['category_nr'].isin(categories[mode]))].to_list()
        
        
    return feature_data, image_path_list