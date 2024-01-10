"""This script creates the lists for fetching the input"""

import os
import random
import argparse
import shutil

def fetch_files(folder_path):
    return [file for file in os.listdir(folder_path) if file.endswith(('.npz', '.npy.h5'))]

def extract_file_names(npz_files):
    return [os.path.splitext(file)[0] for file in npz_files]

def write_to_file(file_names, output_file):
    with open(output_file, 'w') as f:
        f.write('\n'.join(file_names))

def sample_random_inputs(folder_path, num_samples):
    npz_files = fetch_files(folder_path)
    sampled_files = random.sample(npz_files, min(num_samples, len(npz_files)))
    return extract_file_names(sampled_files)

def create_lists(dataset_name, folder_path, num_samples, train_folder_path, test_folder_path):
    output_folder = f'../lists/lists_{dataset_name}'
    train_output_file = os.path.join(output_folder, 'train.txt')
    test_vol_output_file = os.path.join(output_folder, 'test_vol.txt')

    if os.path.exists(output_folder):
        print(f"Folder 'lists_{dataset_name}' already exists. Deleting existing folder.")
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    train_samples = sample_random_inputs(train_folder_path, num_samples)
    test_vol_files = fetch_files(test_folder_path)

    write_to_file(train_samples, train_output_file)
    write_to_file(test_vol_files, test_vol_output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create lists for fetching input')
    parser.add_argument('--dataset_name', type=str, help='Name of the dataset')
    parser.add_argument('--folder_path', type=str, help='Project root directory path')
    parser.add_argument('--num_samples', type=int, help='Desired number of samples for few shot training')
    parser.add_argument('--trainset_folder_path', type=str, help='Path to the trainset folder')
    parser.add_argument('--testset_folder_path', type=str, help='Path to the testset folder')

    args = parser.parse_args()

    create_lists(args.dataset_name, args.folder_path, args.num_samples, args.trainset_folder_path, args.testset_folder_path)