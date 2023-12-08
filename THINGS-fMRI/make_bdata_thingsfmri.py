from typing import Union

import os
from pathlib import Path
import csv

import bdpy
import numpy as np
import pandas as pd


PathType = Union[str, Path]


def make_bdata_things(data_f: PathType, stim_f: PathType, meta_f: PathType, output_file: PathType):
    """Make BData files for THINGS-fMRI dataset."""
    print("Source data:")
    print(f"\t{data_f}")
    print(f"\t{stim_f}")
    print(f"\t{meta_f}")

    # Load voxel metadata and stimulus
    with open(stim_f, 'r') as f:
        reader = csv.DictReader(f)
        stims = [row for row in reader]
    #print(len(stims))

    with open(meta_f, 'r') as f:
        reader = csv.DictReader(f)
        voxels = [row for row in reader]
    #print(len(voxels))

    n_trials = len(stims)
    n_voxels = len(voxels)

    # Load fMRI data
    resp = pd.read_hdf(data_f)
    print("fMRI data size: ", resp.shape)

    # Dataset
    voxel_data_lst = []
    trial_id = np.array([])
    trial_type = np.array([])
    run = np.array([])
    session = np.array([])
    stimulus_name = np.array([])

    for stim in stims:
        _trial_id = int(stim['trial_id'])
        _session = int(stim['session'])
        _run = int(stim['run'])
        _trial_type = stim['trial_type']  # "train" or "test"
        _stimulus_name = os.path.splitext(stim['stimulus'])[0]

        _trial_resp = resp[_trial_id].values

        voxel_data_lst.append(_trial_resp)
        trial_id = np.append(trial_id, _trial_id)
        trial_type = np.append(trial_type, _trial_type)
        run = np.append(run, _run)
        session = np.append(session, _session)
        stimulus_name = np.append(stimulus_name, _stimulus_name)

    voxel_data = np.vstack(voxel_data_lst)
    print("VoxelData size: ", voxel_data.shape)

    # Fix run numbers
    run_inc = np.hstack(
        [
            np.repeat(
                run[(session == n).flatten()][-1],
                np.sum(session == n)
            )
            for n in np.unique(session)
        ]
    )
    run = run + run_inc[:] * (session - 1)
    print("Run: ", np.unique(run))

    # Voxel metadata
    metadatas = {k: np.zeros(n_voxels) for k in voxels[0]}
    for i, voxel in enumerate(voxels):
        for k, v in voxel.items():
            metadatas[k][i] = float(v)

    # Stimulus name vmap setup
    stimulus_set = np.unique(stimulus_name)
    stimulus_name_vmap = {i: s for i, s in enumerate(stimulus_set)}
    stimulus_name_rvmap = {s: i for i, s in enumerate(stimulus_set)}
    #print(len(stimulus_name_vmap))
    #print(len(stimulus_name_rvmap))
    stimulus_name_numeral = np.array([stimulus_name_rvmap[x] for x in stimulus_name])

    # Trial type vmap setup
    trial_type_rvmap = {'train': 1, 'test': 2}
    trial_type_vmap = {v: k for k, v in trial_type_rvmap.items()}
    trial_type_numeral = np.array([trial_type_rvmap[x] for x in trial_type])

    # Make BData
    bdata = bdpy.BData()

    bdata.add(voxel_data, 'VoxelData')
    bdata.add(trial_id, 'trial_id')
    bdata.add(session, 'session')
    bdata.add(run, 'run')
    bdata.add(trial_type_numeral, 'trial_type')
    bdata.add_vmap('trial_type', trial_type_vmap)
    bdata.add(stimulus_name_numeral, 'stimulus_name')
    bdata.add_vmap('stimulus_name', stimulus_name_vmap)

    for k, v in metadatas.items():
        bdata.add_metadata(k, v, where='VoxelData')

    bdata.save(output_file)
    print(f"Saved {output_file}")


if __name__ == "__main__":
    src_dir = Path('./src/fMRI-Single-Trial-Responses-table-format/betas_csv')

    subs = ['sub-01', 'sub-02', 'sub-03']

    for sub in subs:
        data_f = src_dir / f"{sub}_ResponseData.h5"
        stim_f = src_dir / f"{sub}_StimulusMetadata.csv"
        meta_f = src_dir / f"{sub}_VoxelMetadata.csv"

        output_file = Path("output") / f"{sub}.h5"

        make_bdata_things(data_f, stim_f, meta_f, output_file)
