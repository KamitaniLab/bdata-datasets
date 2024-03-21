
import os
import shutil
import logging
from typing import List


def save_codes(cwd: str, hydra_cwd: str, dirs: List[str], logger: logging.Logger) -> None:
    """
    Copy files in the specified directories to the hydra directory.
    
    :param cwd: Current working directory.
    :param hydra_cwd: Hydra working directory.
    :param dirs: List of directories to copy.
    :param logger: Logger.
    """
    
    for d in dirs:
        src_dir = os.path.join(cwd, d)
        hydra_replica_dir = os.path.join("replica", d)
        if not os.path.exists(hydra_replica_dir):
            shutil.copytree(src_dir, hydra_replica_dir)
        
    return None