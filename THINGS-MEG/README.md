# THINGS-MEG

## From preprocessed, single-trial data

1. Download preprocessed THINGS-MEG dataset.

```
% sh download.sh
```

This script will download THING-MEG data from [THINGS-data: MEG preprocessed dataset](https://plus.figshare.com/articles/dataset/THINGS-data_MEG_preprocessed_dataset/21215246) in `src/MEG-preprocessed-dataset`.

Resulting files in `src/MEG-preprocessed-dataset/LOCAL`.


`THINGS-MEG_preproc.tar.gz` is no longer necessary and you can remove it.


2. Create train-test splitted Bdata files

```
% python scripts/make.py make_type=preproc

```

This will create the following files. MEG data are splitted into training and test samples and saved in separated files.

```
output
└── _preproc
        ├── sub-01_test.h5
        ├── sub-01_training.h5
        ├── sub-02_test.h5
        ├── sub-02_training.h5
        ├── sub-03_test.h5
        ├── sub-03_training.h5
        ├── sub-04_test.h5
        └── sub-04_training.h5
```

Also, in this THINGS-MEG dataset, category is overlapping with the training and test. Benchetrit et al. (2024) created a new, larger test dataset by incorporating images from test categories that were originally included in the training dataset. This methodology underscores the importance of considering category overlap in dataset construction to enhance the robustness and generalizability of machine learning models. You can change the category overlap settings by following code.

```
% python scripts/make.py make_type=preproc category_overlap=False
```




## From Unpreprocessed, single-trial data with customized settings

1. Download unpreprocessed THINGS-MEG dataset and change `custom/default.yaml` in configs folder.

```
custom:
  bids_dir                    : # the path to the BIDS directory
  l_freq                      : 0.1 # the lower frequency of the band-pass filter (Hz)
  h_freq                      : 40 # the higher frequency of the band-pass filter (Hz)
  pre_stim_time               : -0.5 # the time before the stimulus onset (s)
  post_stim_time              : 1.0 # the time after the stimulus onset (s)
  output_resolution           : 120 # the resampling frequency (Hz)
```


2. Create Bdata files

```
% python scripts/make.py make_type=custom

```

This will create the following file. MEG data are splitted into training and test samples and saved in separated files.

```
data
└── custom_{l_freq}_{h_freq}_{pre_stim_time}_{post_stim_time}_{output_resolution}
        ├── sub-01_test.h5
        ├── sub-01_training.h5
        ├── sub-02_test.h5
        ├── sub-02_training.h5
        ├── sub-03_test.h5
        ├── sub-03_training.h5
        ├── sub-04_test.h5
        └── sub-04_training.h5
```

Also, the category_overlap setting can be changed by just as same as the preprocessed data.