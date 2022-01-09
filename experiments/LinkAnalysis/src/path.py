import os
from pathlib import Path


ROOT_PATH = os.path.abspath(os.path.join(
    os.path.abspath(__file__),
    os.pardir,
    os.pardir
))

DATASET_PATH = os.path.join(ROOT_PATH, 'datasets')

EXPORT_PATH = os.path.join(ROOT_PATH, 'exports')

DATASETS_FILE_NAME = [
    'graph_1.txt',
    'graph_2.txt',
    'graph_3.txt',
    'graph_4.txt',
    'graph_5.txt',
    'graph_6.txt',
]

def get_file_path(filename: str, path: str):
    Path(path).mkdir(parents=True, exist_ok=True)
    return os.path.join(path, filename)