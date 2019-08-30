'''Delete old backup files'''
from datetime import datetime, timedelta
import datefinder
import os
import re
from glob import glob
from contextlib import suppress

def format():
    '''Time format for deleting backup files'''
    time = datetime.now().strftime("%Y-%m-%d")
    return time

def delete_backups():
    '''Delete all logs with .sql name'''
    backup_date = format()

    with suppress(OSError):
        try:
            for files in glob('*.sql'):
                with open(files, 'r') as bfile:
                    bfile_name = os.path.basename(bfile.name)

                    try:
                        dates = list(datefinder.find_dates(bfile_name))
                        if dates is not None:
                            for date in dates:
                                new_date = date.strftime("%Y-%m-%d")

                                if new_date < backup_date:
                                    try:
                                        os.remove(files)
                                        print('Removed past files only')
                                    except:
                                        print('Error removing files')
                                else:
                                    print('Files can only be deleted after 48 hours')
                        else:
                            print('No backups from 2 days ago')
                    except:
                        print('File doesnt have that group')
        except Exception as error:
            print('Error occured: ', error)

# Unused Important Code
# match = re.search(r'\d{4}-\d{2}-\d{2}', bfile_name)
# date = datetime.strptime(match.group(), '-%Y-%m-%d-%H-%M-%S').date()

