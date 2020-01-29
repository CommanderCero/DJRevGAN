@echo off
set /p user="Enter username: "
set /p password="Enter password for %user%: "

@echo on
python download_dataset.py --download_path=cbct_data --project_id=DELTA_RADIOMICS_LUNG_CBCT --username=%user% --password=%password%
pause