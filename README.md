# Clean Downloads

## Scope

This script aims to organise items in the downloads folder by sorting them in an _archives_ folder.

## Usage

At the bottom of the script, change the parameters in the function call `cleanDownloadsFolder(7, 30)` to suit your preference.

The first value is the age in days to archive from. If the file was created more than this number of days, it will be archived.

The second value is the age in days to delete from. If the file was created more than this number of days, it will be deleted from the archives.

## Run at Startup

See https://apple.stackexchange.com/questions/307812/run-python-script-on-computer-boot