import xnat
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--download_path", help="Provide path where the files are downloaded", default=".")
parser.add_argument("--project_id", help="Provide ID for the XNAT project to download images", default="stwstrategyln1")
parser.add_argument("--username", help="Provide your username to gain access to private projects.", default=None)
parser.add_argument("--password", help="Provide your password for your user.", default=None)
args = parser.parse_args()

with xnat.connect('https://xnat.bmia.nl', user=args.username, password=args.password) as session:
    if not(os.path.isdir(args.download_path)):
        os.mkdir(args.download_path)
    
    existing_subjects = os.listdir(args.download_path)
    project = session.projects[args.project_id]
    print(f'Total number of subjects {len(project.subjects)}')
    for i, subject in enumerate(project.subjects.values()):
        
        if subject.label in existing_subjects:
            print(f'{i+1}/{len(project.subjects)}: Skipping {subject.label} since it already exists in the target folder.')
        else:
            print(f'{i+1}/{len(project.subjects)}: {subject.label} downloading {len(subject.experiments)} experiment(s)')
            subject.download_dir(args.download_path)