#!/bin/sh

set -Ceu

if [ ! -e "./src/fMRI-Single-Trial-Responses-table-format/betas_csv" ]; then
    #wget https://plus.figshare.com/ndownloader/files/36789690 -O ./src/fMRI-Single-Trial-Responses-table-format/betas_csv.tar.gz
    tar xzvf ./src/fMRI-Single-Trial-Responses-table-format/betas_csv.tar.gz -C ./src/fMRI-Single-Trial-Responses-table-format
fi
