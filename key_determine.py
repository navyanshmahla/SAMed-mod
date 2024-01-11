"""This script can be used to determine the number of keys with their names and size of tensor in each key"""

import h5py

file_path = 'BraTS20_Training_369.npy.h5' #accordingly change the file path

with h5py.File(file_path, 'r') as file:
    keys = list(file.keys())
    print("Keys in the HDF5 file:", keys)

    for key in keys:
        dataset = file[key] 
        print(f"Dataset: {key}, Size: {dataset.shape}")
