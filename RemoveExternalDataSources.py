from pathlib import Path
from zipfile import ZipFile
import os
import shutil
from BacpacTools import BacpacContentTool

in_dir = './in'
working_dir = './working'
out_dir = './out'
processed_dir = './processed'

paths = [in_dir, working_dir, out_dir, processed_dir]

model_path = 'model.xml'

for path in paths:
    Path(path).mkdir(parents=True, exist_ok=True)

files_to_process = [path for path in Path(in_dir).iterdir() if path.suffix == '.bacpac']

if len(files_to_process) == 0:
    print(f'Setup complete, no files found to process')

working_trash = [path for path in Path(working_dir).iterdir()]
if len(working_trash) != 0:
    print(f'Found working files, cleaning them up')
    shutil.rmtree(working_dir)
    Path(working_dir).mkdir(parents=True, exist_ok=True)

for file in files_to_process:
    print(f'Working on {file.name}')
    file_stem = file.stem
    with ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(working_dir)

    with BacpacContentTool(working_dir) as bpt:
        bpt.remove_external_data_sources()
        bpt.remove_external_tables()

    out_file = Path(out_dir) / f'{file_stem}_localsafe.bacpac'
    with ZipFile(out_file, 'w') as zip_ref:
       for folder_name, subfolders, file_names in os.walk(working_dir):
           for file_name in file_names:
               file_path = os.path.join(folder_name, file_name)
               zip_ref.write(file_path, Path().joinpath(*Path(file_path).parts[1:]))
    
    #os.rename(file, Path(processed_dir) / file.name)
    shutil.rmtree(working_dir)
    Path(working_dir).mkdir(parents=True, exist_ok=True)
    print(f'Done with {file.name}')
    