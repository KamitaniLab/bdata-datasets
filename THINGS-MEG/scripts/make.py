from src.make_bdata_thingsmeg import make_bdata_thingsmeg
from src.preproc_thingsmeg import preproc_thingsmeg
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
from src.utils.codes import save_codes
from src.utils.record import setup_logging



@hydra.main(config_path="../configs", config_name="make")
def make(cfg: DictConfig) -> None:
    
    setup_logging()
    logger = logging.getLogger(__name__)

    ### Initial settings --------------------------------------------------------
    ## analysis name
    if cfg.make_type == "preproc":
        analysis_name = "_preproc"
    else:
        analysis_name = f"custom_{cfg.custom.l_freq}_{cfg.custom.h_freq}_{cfg.custom.pre_stim_time}_{cfg.custom.post_stim_time}_{cfg.custom.output_resolution}"
    
    logger.info(f"analysis name: {analysis_name}")
    
    ## Directory check
    cwd = hydra.utils.get_original_cwd()
    hydra_cwd = hydra.core.hydra_config.HydraConfig.get().run.dir
    
    logger.info(f"Original cwd: {cwd}")
    logger.info(f"Hydra cwd: {hydra_cwd}")
    
    ## Check whether the output is already there 
    output_dir = os.path.join(cwd, 'data', analysis_name)
    if os.path.exists(output_dir) and cfg.overwrite == False:
        logger.info(f"Output directory {output_dir} already exists. Skip processing.")
        return
    
    ## save codes for replica
    save_codes(cwd, hydra_cwd, ["src", "scripts", "configs"], logger)
    
    ### DO ---------------------------------------------------------------------
    for participant in cfg.participants:
        preproc_data = preproc_thingsmeg(cfg, participant, logger)
        make_bdata_thingsmeg(cfg, participant, preproc_data, output_dir, logger)
        
        logger.info(f"Participant {participant} done.")
    
    ### Save reference ----------------------------------------------------------
    # 実行時のhydraのディレクトリをoutput_dirにtxtで上書き保存
    with open(os.path.join(output_dir, "hydra_cwd.txt"), "a") as f:
        f.write(hydra_cwd + "\n")


if __name__ == "__main__":

    make()