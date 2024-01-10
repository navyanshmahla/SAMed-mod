"""This script does the pre-processsing of data for creating testset"""

import os
import SimpleITK as sitk
import numpy as np
import h5py

# Function to convert NIfTI to NumPy array
def nifti_to_numpy(file_path):
    img = sitk.ReadImage(file_path)
    img_array = sitk.GetArrayFromImage(img)
    return img_array

# Source and target directories
source_dir = '../BraTS20/BraTS2020_TrainingData/MICCAI_BraTS2020_TrainingData'
target_dir = '../testset/brats20_testset'

# Iterate through source subfolders
for subdir in os.listdir(source_dir):
    subdir_path = os.path.join(source_dir, subdir)
    if os.path.isdir(subdir_path):
        t1_file = os.path.join(subdir_path, f'{subdir}_t1.nii')
        seg_file = os.path.join(subdir_path, f'{subdir}_seg.nii')

        # Check if both files exist
        if os.path.exists(t1_file) and os.path.exists(seg_file):
            # Convert NIfTI to NumPy arrays
            t1_array = nifti_to_numpy(t1_file)
            seg_array = nifti_to_numpy(seg_file)

            # Create an HDF5 file and store NumPy arrays
            target_file = os.path.join(target_dir, f'{subdir}.npy.h5')
            with h5py.File(target_file, 'w') as hf:
                hf.create_dataset('image', data=t1_array)
                hf.create_dataset('seg', data=seg_array)
    
    print(f"Done for file with dir: {subdir_path}")

print("Done for all the files!")
