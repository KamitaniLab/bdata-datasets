import os
import copy

import bdpy


dir_path = "./output"
subjects = ['sub-01', 'sub-02', 'sub-03']


for sub in subjects:
    print(sub)

    src_bdata = bdpy.BData(os.path.join(dir_path, f"{sub}.h5"))

    print("Training data")
    train_bdata = copy.deepcopy(src_bdata)
    train_index = src_bdata.select('trial_type') == 1
    train_bdata.dataset = train_bdata.dataset[train_index.flatten(), :]
    print(train_bdata.dataset.shape)
    train_bdata.save(os.path.join(dir_path, f"{sub}_training.h5"))
    del(train_bdata)

    print("Test data")
    test_bdata = copy.deepcopy(src_bdata)
    test_index = src_bdata.select('trial_type') == 2
    test_bdata.dataset = test_bdata.dataset[test_index.flatten(), :]
    print(test_bdata.dataset.shape)
    test_bdata.save(os.path.join(dir_path, f"{sub}_test.h5"))
    del(test_bdata)
