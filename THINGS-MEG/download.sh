#!/bin/sh

set -Ceu

if [ ! -e "./src/MEG-preprocessed-dataset/THINGS-MEG_preproc" ]; then
    wget https://plus.figshare.com/ndownloader/files/39472855 -O ./src/MEG-preprocessed-dataset/THINGS-MEG_preproc.tar.gz
    tar xzvf ./src/MEG-preprocessed-dataset/THINGS-MEG_preproc.tar.gz
fi

