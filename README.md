# AL_elections_data
A script to download all zip, excel, and PDFs from the [Alabama Secretary of State Elections Data Downloads page](https://www.sos.alabama.gov/alabama-votes/voter/election-data).

## instructions

 1. create a directory for the data
 2. download and edit `download_script.py` to account for your directory
 3. run `download_script.py`, this will download all the zip, excel, and PDF files from the AL SOS page above and unzip the .zips into their own folders.
 4. run `naming_cleanup_script.py`, this will clean up the file and folder names
 5. run `ALVR_script_v11.py` to investigate the tab names and header info of each ALVR excel file. (note the inconsistencies) 
 6. enjoy the data!
