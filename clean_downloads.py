import getpass
import logging
import os
from datetime import datetime


def cleanDownloadsFolder(archiveAge, deleteAge):

    # Get paths and variables
    username = getpass.getuser()
    downloadsFolder = '/Users/%s/Downloads' % username
    archivesFolder = '%s/Archives' % downloadsFolder
    logsFolder = '%s/logs' % archivesFolder
    currentTime = datetime.now()
    logFile = '%s/logs/%s%s%s_%s%s.log' % (archivesFolder,
                                           currentTime.year, currentTime.month, currentTime.day, currentTime.hour, currentTime.minute)

    # Create the logs folder if it does not exist
    if not os.path.isdir(logsFolder):
        os.mkdir(logsFolder)

    # Configure the logging agent
    logging.basicConfig(filename=logFile, level=logging.DEBUG)

    # Log some variables
    logging.info('Current user: %s' % username)
    logging.info('Current Time: %s' % currentTime)

    # Create the Archives folder if it does not exist
    if not os.path.isdir(archivesFolder):
        os.mkdir(archivesFolder)
        logging.info('Created Archives directory.')

    # Get folder items
    downloadsItems = os.listdir(downloadsFolder)
    #archivesItems = os.listdir(archivesFolder)

    # Move old items to Archives
    downloadsItems.remove('Archives')
    if (len(downloadsItems) > 0):
        for item in downloadsItems:
            if not item.startswith('.'):
                fPath = '%s/%s' % (downloadsFolder, item)
                faPath = '%s/%s' % (archivesFolder, item)
                fAge = currentTime - \
                    datetime.fromtimestamp(os.path.getmtime(fPath))
                if (int(fAge.days) > archiveAge):
                    try:
                        os.rename(fPath, faPath)
                        logging.info('Moved %s to Archives' % item)
                    except Exception as E:
                        logging.error('Unable to move %s to Archives' % item)
                        logging.error(E)
    else:
        logging.info('No files in downloads folder')

    # Iterate through all the archive keys and add files to archivesItems list
    archivesItems = []
    for yearFolder in os.listdir(archivesFolder):
        if yearFolder != 'logs' and os.path.isdir(yearFolder):
            for monthFolder in os.listdir('%s/%s' % (archivesFolder, yearFolder)):
                for dayFolder in os.listdir('%s/%s/%s' % (archivesFolder, yearFolder, monthFolder)):
                    for item in os.listdir('%s/%s/%s/%s' % (archivesFolder, yearFolder, monthFolder, dayFolder)):
                        fPath = '%s/%s/%s/%s/%s' % (archivesFolder, yearFolder, monthFolder, dayFolder, item)
                        fileDict = {
                            'name': item,
                            'path': fPath
                        }
                        archivesItems.append(fileDict)

    if (len(archivesItems) > 0):
        sortArchiveFolder = '%s/%s/%s/%s' % (archivesFolder, currentTime.year, currentTime.month, currentTime.day)
        if not os.path.isdir(sortArchiveFolder):
            os.mkdir(sortArchiveFolder)
            logging.info('Created archive folder for %s' % currentTime)
        for item in archivesItems:
            fAge = currentTime - \
                datetime.fromtimestamp(os.path.getmtime(item['path']))
            if (int(fAge.days) > deleteAge):
                try:
                    os.remove(fPath)
                    logging.warning('Permanently deleted %s' % item['name'])
                except Exception as E:
                    logging.error('Unable to delete %s' % item['name'])
                    logging.info(E)
    else:
        logging.info('No files in archives')


if __name__ == "__main__":
    # cleanDownloadsFolder(a, b)
    # a: Files in /Downloads not modified for this number of days are moved to /Downloads/Archives
    # b: Files in /Downloads/Archives not modified for this number of days are deleted
    cleanDownloadsFolder(7, 30)
