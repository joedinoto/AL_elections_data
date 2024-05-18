import os
import shutil

def replace_space_and_dash_with_space_and_convert_year(folder_path):
    # Walk through the directory structure
    for root, dirs, files in os.walk(folder_path):
        for directory in dirs:
            # Check if the folder name contains %20 or -
            if '%20' in directory or '-' in directory:
                # Replace %20 and - with a space
                new_name = directory.replace('%20', ' ').replace('-', ' ')
                old_path = os.path.join(root, directory)
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed '{directory}' to '{new_name}'")
            
            # Check if the folder name starts with two digits and does not follow the yyyy format
            if directory[:2].isdigit() and not directory[:4].isdigit():
                # Interpret the first two digits as a year and rename the folder accordingly
                year = int(directory[:2])
                if 0 <= year <= 50:
                    year += 2000
                else:
                    year += 1900
                new_name = f"{year}{directory[2:]}"
                old_path = os.path.join(root, directory)
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed '{directory}' to '{new_name}'")
                
            # Check if the folder name is a four-digit year followed by a non-space character
            if len(directory) >= 5 and directory[:4].isdigit() and directory[4] != ' ':
                # Insert a space after the year
                new_name = f"{directory[:4]} {directory[4:]}"
                old_path = os.path.join(root, directory)
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed '{directory}' to '{new_name}'")

        for file in files:
            if file.endswith('.zip'):
                zip_dir = os.path.join(root, "zz zip files")
                os.makedirs(zip_dir, exist_ok=True)
                old_path = os.path.join(root, file)
                new_path = os.path.join(zip_dir, file)
                shutil.move(old_path, new_path)
                print(f"Moved '{file}' to 'zz zip files'")
            elif file.endswith('.pdf'):
                pdf_dir = os.path.join(root, "zz pdf files")
                os.makedirs(pdf_dir, exist_ok=True)
                old_path = os.path.join(root, file)
                new_path = os.path.join(pdf_dir, file)
                shutil.move(old_path, new_path)
                print(f"Moved '{file}' to 'zz pdf files'")

# Specify the folder path where you want to perform replacements
folder_path = "/home/linuxlaptop/Documents/AL_elections/data"

# Call the function to perform replacements
replace_space_and_dash_with_space_and_convert_year(folder_path)

