import os

RESOURCE_TYPE_DICOM = "DICOM"
RESOURCE_TYPE_MASK = "secondary"

def get_resource_type(file_path):
    parts = file_path.split(os.sep)
    # We assume that the last 3 parts of our file path are as follows
    # <resource_type>/files/<dicom_file_name>.dcm
    resource_type = parts[-3]
    
    if resource_type not in [RESOURCE_TYPE_DICOM, RESOURCE_TYPE_MASK]:
        raise Exception(f"Unexpected resource_type '{resource_type}' for {file_path}. Expected {RESOURCE_TYPE_DICOM} or {RESOURCE_TYPE_MASK}.")
        
    return resource_type

def get_scan_folder_name(file_path):
    parts = file_path.split(os.sep)
    # We assume that the last 5 parts of our file path are as follows
    # <scan_name>/resources/<resource_type>/files/<dicom_file_name>.dcm
    scan_folder_name = parts[-5]
    
    return scan_folder_name