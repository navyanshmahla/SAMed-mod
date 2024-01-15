import os
import numpy as np
import nibabel as nib
import argparse
import h5py

def load_nifti_data(file_path):
    return nib.load(file_path).get_fdata()

def normalize_data(data):
    data = np.clip(data, -125, 275)
    return (data - (-125)) / (275 - (-125))

def transpose_data(data):
    return np.transpose(data, (2, 1, 0))

def process_subfolder(sub_folder, output_folder):
    t1_file = os.path.join(sub_folder, f'{os.path.basename(sub_folder)}_t1.nii')
    seg_file = os.path.join(sub_folder, f'{os.path.basename(sub_folder)}_seg.nii')

    if os.path.exists(t1_file) and os.path.exists(seg_file):
        t1_data = load_nifti_data(t1_file)
        seg_data = load_nifti_data(seg_file)

        t1_data = normalize_data(t1_data)
        t1_data = transpose_data(t1_data)
        seg_data = transpose_data(seg_data)

        os.makedirs(output_folder, exist_ok=True)

        output_path = os.path.join(output_folder, f'{os.path.basename(sub_folder)}.npy.h5')
        with h5py.File(output_path, 'w') as h5file:
            h5file.create_dataset('image', data=t1_data)
            h5file.create_dataset('label', data=seg_data)

def preprocess_dataset(main_folder, output_folder):
    for subdir in os.listdir(main_folder):
        sub_folder = os.path.join(main_folder, subdir)

        if os.path.isdir(sub_folder):
            process_subfolder(sub_folder, output_folder)
            print(f"Done for the sub folder with path: {sub_folder}")

    print(f"Pre-processing complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pre-process the dataset')
    parser.add_argument('--main_folder', type=str, help='Path to the main folder containing the dataset')
    parser.add_argument('--output_folder', type=str, help='Output folder to store processed data')

    args = parser.parse_args()

    preprocess_dataset(args.main_folder, args.output_folder)
