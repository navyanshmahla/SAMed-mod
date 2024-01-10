# SAMed Custom Dataset Implementation

This repo has been adopted from [this repo](https://github.com/hitachinsk/SAMed/tree/main) which aims to implement [this paper](https://arxiv.org/pdf/2304.13785.pdf).

This repo is a small cross modification for training/fine-tuning SAMed for custom dataset. 

Details for implementation on Synapse multi-organ dataset can be found at the original repo. This repository aims to use BraTS 2020 dataset as dataset. 

# Pre-requisites

Running this repo requires:

- Linux
- Any conda based environment and package management tool (Anaconda or Miniconda)
- Python 3.7.11
- PyTorch 1.9.1

## Setting Up the Repo

Get started by cloning the repository locally and setup the conda environment as follows:

```shell
conda create -n SAMed python=3.7.11
conda activate SAMed
pip install -r requirements.txt
```

Sometimes while installing the `requirements.txt` file, errors related to PyTorch installation might occur, in that case use the below command to install PyTorch separately and then run the `requirements.txt` for installation.

```shell
pip install torch==1.9.1+cu111 torchvision==0.10.1+cu111 torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html
```

## Setting Up the dataset

Scripts to pre-process the dataset are present in the `utils` folder. The project requires an archived multi key numpy array to save the image and labels together which are then later processed once you hit train. For that reason its important to pre-process the files to `.npz` format which is the only acceptable format for this repo.

```shell
python pre-process_train.py --main_folder /relative/path/to/raw/dataset --output_folder /relative/path/to/output_folder
```

> Pre-processing of raw dataset must be done keeping in account of transposition and normalisation. The 3D medical image representation of the data must be converted into 2D image using the slicing. Similarly, its important to do the normalisation of the dataset as shown in the file `pre-process_train.py` other wise the input batch tensor might overflow over the restricted value (which is 3 here).

After pre-processing, you need to mention the names of the train files in the lists from where they're sampled to train under few shot regimes. This similar list creation must be done for testing as well.

```shell
python list_create.py --dataset_name your_dataset_name --folder_path /relative/path/to/root/directory --num_train_samples num_samples --num_test_samples num_samples --trainset_folder_path /realtive/path/to/trainset --testset_folder_path /relative/path/to/testset
```

Once the dataset is set, start the training:

```shell
python3 train.py --root_path ./trainset --output ./BraTS_output --dataset BraTS --list_dir ./lists/lists_BRATS --max_epochs 2 --img_size 240  --warmup --AdamW 
```
Make sure to add the correct relative paths to the datasets and lists.

Train script arguments are present in `train.py` file. You should try your experiments changing the required arguments (hyperparams) for knowing the optimised hyperparams during training. A few of those include epochs, iterations, learning rate, batch size, number of classes, image size, LoRA rank, etc.

## Running Inference

Inferences can be easily run on Synapse multi organ dataset. But the inference requiring other datasets cannot simply use the `test.py` because of different classes and modalities. 

## To Do

- [x] Make necessary modifications in the repo for custom dataset input
- [x] Personalize the scripts in the `./utils` folder
- [ ] Modify the `test.py` file for datasets other than synapse 
