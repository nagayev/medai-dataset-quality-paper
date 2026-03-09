import nibabel as nib
import numpy as np
img = nib.load('native_shuffled.nii')
data = img.get_fdata()
print(f"Форма данных (shape): {data.shape}")