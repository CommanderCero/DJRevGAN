from . import utils
import os
import os.path as path
import glob

class Experiment:
    def __init__(self, patient_folder, experiment_folder, slice_paths, mask_paths):
        self.patient_folder = patient_folder
        self.experiment_folder = experiment_folder
        
        self.name = path.basename(experiment_folder)
        self.patient_id = path.basename(patient_folder)
        
        self.slice_paths = slice_paths
        self.mask_paths = mask_paths

class DCMIterator:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        
    def get_slice_iter(self):
        for dcm_path in glob.glob(os.path.join(self.folder_path, "**/*.dcm"), recursive=True):
            if utils.get_resource_type(dcm_path) == utils.RESOURCE_TYPE_DICOM:
                yield dcm_path
        
    def __iter__(self):
        for patient_folder in os.listdir(self.folder_path):
            full_path = path.join(self.folder_path, patient_folder)
            
            for experiment in self._iterate_experiments_(full_path):
                yield experiment
    
    def _iterate_experiments_(self, patient_folder):
        # There can be multiple experiments for a single patient
        for experiment_folder_name in os.listdir(patient_folder):
            experiment_folder = path.join(patient_folder, experiment_folder_name)
            
            # Find all dicom files in our experiment folder
            dcm_search_pattern = os.path.join(experiment_folder, "**/*.dcm")
            dcm_file_paths = glob.glob(dcm_search_pattern, recursive=True)
            
            # Seperate the dicom-files to slices and the mask file
            slice_paths, mask_paths = self._get_slices_and_mask_(dcm_file_paths)
            
            # Return the experiment
            yield Experiment(patient_folder, experiment_folder, slice_paths, mask_paths)
        
    # TODO Clean this up and split finding the dicom files from searching for the mask path
    def _get_slices_and_mask_(self, dicom_file_paths):
        last_slice_folder = None
        slices = []
        masks = []
        for file_path in dicom_file_paths:
            resource_type = utils.get_resource_type(file_path)
            scan_folder = utils.get_scan_folder_name(file_path)
            
            if resource_type == utils.RESOURCE_TYPE_DICOM:
                if last_slice_folder is None:
                    last_slice_folder = scan_folder
                elif last_slice_folder != scan_folder:
                    continue # For now we will ignore multiple scan folders per experiment
                    
                slices.append(file_path)
                
            elif resource_type == utils.RESOURCE_TYPE_MASK:
                masks.append(file_path)
        
        return slices, masks