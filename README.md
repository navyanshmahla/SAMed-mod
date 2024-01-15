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

**NOTE** : All the pre-processing scripts are written taking in account of the 3D nature of medical dataset samples. If you happen to use this repo for 2D datasets, you must accordingly change the pre-process code by just scrapping off the part where it loads `.nii.gz` files. Instead, directly store the 2D images and labels inside of the numpy archive (either `.npz` or `.npy.h5`). This you'll be good to go with the 2D dataset as well.

Scripts to pre-process the dataset are present in the `utils` folder. The project requires an archived multi key numpy array to save the image and labels together which are then later processed once you hit train. For that reason its important to pre-process the files to `.npz` format which is the only acceptable format for this repo.

It is important to note that the pre-process scripts are written keeping in mind the 3D medical datasets. In case of 2D dataset

```shell
python pre-process_train.py --main_folder /relative/path/to/raw/dataset --output_folder /relative/path/to/output_folder
```

To pre-process the test dataset use the following command:

```shell
python pre_process_test.py --source_dir /relative/path/to/testdata --target_dir ../testset/test_vol_h5
```
**IMP** Have a look at the pre-processing files to have a better idea of how its working. The pre-processing of the data is very specific to the dataset you plan on to use. 

Please note that the target directory (directory where the pre-processed test dataset should be saved) should always be `testset/test_vol_h5` with reference to the project root directory. 

> Pre-processing of raw dataset must be done keeping in account of transposition and normalisation. The 3D medical image representation of the data must be converted into 2D image using the slicing. Similarly, its important to do the normalisation of the dataset as shown in the file `pre-process_train.py` other wise the input batch tensor might overflow over the restricted value (which is 3 here).

**IMP** : The repo works by creating a dataloader for both train and test by fetching the names of the files from the `lists` directory. List corresponding to your dataset must be present in the subdirectory folder. See this repo which contains the lists for Synapse and BraTS20 dataset. 

You can use the below command to create lists. 

```shell
python list_create.py --dataset_name your_dataset_name --folder_path /relative/path/to/root/directory --num_train_samples num_samples --num_test_samples num_samples --trainset_folder_path /realtive/path/to/trainset --testset_folder_path /relative/path/to/testset
```
While running the above command for creating lists it is expected that the trainset folder contains all of your train files in `.npz` format. In case of 3D data it must also have all the slices (which would eventually be created if the dataset is 3D and you use the given pre-processing script). 

Once the dataset is set, start the training:

```shell
python3 train.py --root_path ./trainset --output ./BraTS_output --dataset BraTS --list_dir ./lists/lists_BRATS --max_epochs 2 --img_size 240  --warmup --AdamW 
```
Make sure to add the correct relative paths to the datasets and lists.

Train script arguments are present in `train.py` file. You should try your experiments changing the required arguments (hyperparams) for knowing the optimised hyperparams during training. A few of those include epochs, iterations, learning rate, batch size, number of classes, image size, LoRA rank, etc.

## Running Inference

Inferences can be easily run on Synapse multi organ dataset. But the inference requiring other datasets cannot simply use the `test.py` because of different classes and modalities. 

To run the inference :

```shell
python test.py --is_savenii --dataset BraTS --num_classes num_classes --list_dir ./lists/lists_BraTS20 --output_dir ./test_output --img_size size_of_img --lora_ckpt /relative/path/to/lora/chkpt
```

## To Do

- [x] Make necessary modifications in the repo for custom dataset input
- [x] Personalize the scripts in the `./utils` folder
- [x] Modify the `test.py` file for datasets other than synapse 
- [ ] Probably make a script to determine normalisation parameters in `./utils/pre_process_test.py` and `./utils/pre_process_train.py`
