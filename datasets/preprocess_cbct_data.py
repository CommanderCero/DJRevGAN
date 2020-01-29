import os
from tqdm import tqdm

from dcm_iterator import DCMIterator
import pydicom
import numpy as np

def generate_train_flags(size, test_size=0.2):
    """
        Generates a array containing randomly placed ones and zeroes
        This array will be later used to indicate if a DICOM-File is used for training or testing
        
        test_size specifies the amount of test files should be included, relative to size
    """
    flags = np.ones(size)
    test_idx = np.random.randint(low=0, high=size, size=int(size*test_size))
    flags[test_idx] = 0
    
    return flags

# We want the HU values of our Image, but the pixel_array from the DICOM does not contain the HU values
# This method converts the pixel_arrays to HU-values
def get_hu_pixel_array(s):
    img = s.pixel_array.astype(np.float64)
    img *= s.RescaleSlope
    img += s.RescaleIntercept
    
    return img.astype(np.int16)    

def preprocess_slices(slice_paths, target_folder, dataset_name, progressbar, test_size=0.2):
    train_flags = generate_train_flags(len(slice_paths), test_size=test_size)
    
    for slice_path, train_flag in tqdm(zip(slice_paths, train_flags)):
        # Preprocess
        data = pydicom.dcmread(slice_path)
        img_data = get_hu_pixel_array(data)
        
        # Save to disk
        file_name = f"{data.PatientID}_{data.InstanceNumber}.npy"
        dataset_folder = os.path.join(target_folder, f"{'train' if train_flag else 'test'}{dataset_name}")
        np.save(os.path.join(dataset_folder, file_name), img_data)
        
        # Update progressbar
        progress_bar.update(1)

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description='Preprocesses DICOM-files for the use in an GAN.')
    parser.add_argument('--cbct', help='The folder containing the CBCT data', default="cbct_data")
    parser.add_argument('--ct', help='The folder containing the CT data', default="ct_data")
    parser.add_argument('--targetFolder', help='The folder where the processed data should be saved', default="datasets")
    parser.add_argument('--testSize', type=float, default="0.2")
    args = parser.parse_args()
    
    # Ensure the folders we need exist
    for folder in ["trainA", "trainB", "testA", "testB"]:
        Path(os.path.join(args.targetFolder, folder)).mkdir(parents=True, exist_ok=True)
    
    # Create iterators for CBCT- and CT-data
    cbct_iterator = DCMIterator(args.cbct)
    ct_iterator = DCMIterator(args.ct)
    
    # Preprocess the data
    cbct_slices = list(cbct_iterator.get_slice_iter())
    ct_slices = list(ct_iterator.get_slice_iter())
    
    with tqdm(total=len(cbct_slices)+len(ct_slices), ascii=True) as progress_bar:
        progress_bar.set_description("Preprocessing CBCT-Data")
        preprocess_slices(cbct_slices, args.targetFolder, "CBCT", progress_bar, args.testSize)
        
        progress_bar.set_description("Preprocessing CT-Data")
        preprocess_slices(ct_slices, args.targetFolder, "CT", progress_bar, args.testSize)
    