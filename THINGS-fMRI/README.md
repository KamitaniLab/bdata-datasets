# THINGS-fMRI

## Preprocessed, single-trial, visual areas

1. Downloading THINGS-fMRI dataset.

```
% sh download.sh
```

This script will download THING-fMRI data from [THINGS-data: fMRI Single Trial Responses (table format)](https://plus.figshare.com/articles/dataset/6161151) in `src/THINGS/fMRI-Single-Trial-Responses-table-format`.

Resulting files in `src/THINGS/fMRI-Single-Trial-Responses-table-format/betas_csv`.

```
src
└── fMRI-Single-Trial-Responses-table-format
    ├── betas_csv
    │   ├── sub-01_ResponseData.h5
    │   ├── sub-01_StimulusMetadata.csv
    │   ├── sub-01_VoxelMetadata.csv
    │   ├── sub-02_ResponseData.h5
    │   ├── sub-02_StimulusMetadata.csv
    │   ├── sub-02_VoxelMetadata.csv
    │   ├── sub-03_ResponseData.h5
    │   ├── sub-03_StimulusMetadata.csv
    │   └── sub-03_VoxelMetadata.csv
    └── betas_csv.tar.gz
```

`betas_csv.tar.gz` is no longer necessary and you can remove it.

2. Create Bdata files

```
% python make_bdata_thingsfmri.py

```

This will create the following file. Each file contains fMRI data of each subject.

```
output
├── sub-01.h5
├── sub-02.h5
└── sub-03.h5
```

3. Create train-test splitted BData files

```
% python make_bdata_thingsfmri_traintestsplit.py

```

This will additionally create the following file. fMRI data are splitted into training and test samples and saved in separated files.

```
output
├── sub-01_test.h5
├── sub-01_training.h5
├── sub-02_test.h5
├── sub-02_training.h5
├── sub-03_test.h5
└── sub-03_training.h5
```
