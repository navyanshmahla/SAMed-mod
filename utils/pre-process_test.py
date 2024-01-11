"""This script is to pre-process the raw test dataset"""

import os
import argparse
import SimpleITK as sitk
import numpy as np
import h5py

def nifti_to_numpy(file_path):
    img = sitk.ReadImage(file_path)
    img_array = sitk.GetArrayFromImage(img)
    return img_array

def preprocess_data(source_dir, target_dir):
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
                    hf.create_dataset('label', data=seg_array)

        print(f"Done for file with dir: {subdir_path}")

    print("Done for all the files!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess data for creating a testset.")
    parser.add_argument("--source_dir", required=True, help="Source directory containing NIfTI files.")
    parser.add_argument("--target_dir", required=True, help="Target directory to store processed data.")

    args = parser.parse_args()
    
    preprocess_data(args.source_dir, args.target_dir)
