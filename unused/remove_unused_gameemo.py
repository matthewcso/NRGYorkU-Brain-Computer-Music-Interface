import shutil
from os import listdir
from os.path import join

top_level = 'GAMEEMO'

def rm(target):
    """
    Removes a directory recursively, skipping if there is no such directory.
    Args: 
        target (string): target directory 
    """
    try:
        print('Removing ' + target)
        shutil.rmtree(target)
    except FileNotFoundError:
        print('File '+ target + \
            'not found, skipping')

target = join(top_level, 'Gameplays')
rm(target)

for folder in listdir(top_level):
    target = join(top_level, folder, 'Raw EEG Data', '.mat format')
    rm(target)

    target = join(top_level, folder, 'Preprocessed EEG Data')
    rm(target)

    
