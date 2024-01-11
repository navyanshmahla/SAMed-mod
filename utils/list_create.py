"""
This script creates lists for fetching the input samples for inference/training
"""

import os
import random
import argparse
import shutil
import re

def fetch_files(folder_path):
    return [file for file in os.listdir(folder_path) if file.endswith(('.npz', '.npy.h5'))]

def extract_file_names(npz_files):
    return [os.path.splitext(file)[0] for file in npz_files]

def write_to_file(file_names, output_file):
    with open(output_file, 'w') as f:
        f.write('\n'.join(file_names))

def sample_trainset(folder_path, num_samples):
    indices = set()
    for file in os.listdir(folder_path):
        if file.endswith('.npz'):
            j = file.split('_')[2]
            indices.add(j)

    sampled_indices = random.sample(indices, min(num_samples, len(indices)))
    sampled_files = []
    for idx in sampled_indices:
        files = [f for f in os.listdir(folder_path) if f.startswith(f'BraTS20_Training_{idx}_slice')]
        sampled_files.extend(files)

    return extract_file_names(sampled_files)

def sample_testset(folder_path, trainset_indices, num_samples):
    all_indices = set()
    for file in os.listdir(folder_path):
        if file.endswith('.npy.h5'):
            idx = file.split('_')[2]
            numerical_part = re.search(r'\d+', idx).group()
            all_indices.add(numerical_part)

    available_indices = list(all_indices - set(trainset_indices))
    sampled_indices = random.sample(available_indices, min(num_samples, len(available_indices)))
    
    # Remove the extension '.npy.h5' from the filenames
    sampled_files = [f'BraTS20_Training_{idx}' for idx in sampled_indices]
    
    return sampled_files

def create_lists(dataset_name, folder_path, num_train_samples, num_test_samples, train_folder_path, test_folder_path):
    output_folder = f'../lists/lists_{dataset_name}'
    train_output_file = os.path.join(output_folder, 'train.txt')
    test_vol_output_file = os.path.join(output_folder, 'test_vol.txt')

    if os.path.exists(output_folder):
        print(f"Folder 'lists_{dataset_name}' already exists. Deleting existing folder.")
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    train_samples = sample_trainset(train_folder_path, num_train_samples)
    test_samples = sample_testset(test_folder_path, train_samples, num_test_samples)

    write_to_file(train_samples, train_output_file)
    write_to_file(test_samples, test_vol_output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create lists for fetching input')
    parser.add_argument('--dataset_name', type=str, help='Name of the dataset')
    parser.add_argument('--folder_path', type=str, help='Project root directory path')
    parser.add_argument('--num_train_samples', type=int, help='Desired number of samples for the train set')
    parser.add_argument('--num_test_samples', type=int, help='Desired number of samples for the test set')
    parser.add_argument('--trainset_folder_path', type=str, help='Path to the trainset folder')
    parser.add_argument('--testset_folder_path', type=str, help='Path to the testset folder')

    args = parser.parse_args()

    create_lists(args.dataset_name, args.folder_path, args.num_train_samples, args.num_test_samples, args.trainset_folder_path, args.testset_folder_path)
