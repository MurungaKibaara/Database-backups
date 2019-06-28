'''Delete old logs'''

import os
from glob import glob
from contextlib import suppress

def delete_backups():
    '''Delete all logs with .sql name'''
    with suppress(OSError):
        try:
            for files in glob('*.sql'):
                os.remove(files)
        except Exception as error:
            print('Error occured: ', error)

