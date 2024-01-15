import nibabel as nib
import numpy as np
import os
import matplotlib.pyplot as plt
from skimage.measure import find_contours

def load_nifti_and_show_unique_values(nifti_path, save_path=None):
    # Load the NIfTI file
    nii_img = nib.load(nifti_path)
    nii_data = nii_img.get_fdata()

    # Convert voxel values to integers
    nii_data = np.round(nii_data).astype(int)

    # Display the unique values
    unique_values = np.unique(nii_data)
    print(f"Unique values in {os.path.basename(nifti_path)}: {unique_values}")

    # Visualize the mask
    num_slices = nii_data.shape[-1]
    middle_slice = num_slices // 2
    plt.figure(figsize=(12, 6))
    
    # Plot the NIfTI image slice
    plt.subplot(1, 2, 1)
    plt.imshow(nii_data[:, :, middle_slice], cmap='gray')
    plt.title(f"NIfTI Image Slice: {os.path.basename(nifti_path)}")

    # Plot contours for each unique label
    for label_value in unique_values:
        contours = find_contours(nii_data[:, :, middle_slice] == label_value, 0.5)
        for contour in contours:
            plt.plot(contour[:, 1], contour[:, 0], linewidth=2, label=f'Label {label_value}')

    plt.legend()

    # Plot the histogram of unique values
    plt.subplot(1, 2, 2)
    plt.hist(nii_data.flatten(), bins=len(unique_values), color='c', edgecolor='k')
    plt.title("Histogram of Unique Values")
    plt.xlabel("Unique Values")
    plt.ylabel("Frequency")

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

# Specify the path to the NIfTI file
nifti_path = "./BraTS20/BraTS2020_TrainingData/MICCAI_BraTS2020_TrainingData/BraTS20_Training_129/BraTS20_Training_129_seg.nii"
output_path = "./output_plot.png"  # Specify the desired output path
load_nifti_and_show_unique_values(nifti_path, save_path=output_path)
