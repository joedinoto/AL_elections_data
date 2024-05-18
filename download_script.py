import requests
from bs4 import BeautifulSoup
import os
import zipfile

# URL of the webpage
url = "https://www.sos.alabama.gov/alabama-votes/voter/election-data"

# Set to keep track of downloaded files
downloaded_files = set()

# Function to download files
def download_file(url, directory):
    # Get the file name from the URL
    file_name = url.split("/")[-1]
    # Check if the file has already been downloaded
    if file_name in downloaded_files:
        print(f"Skipping {file_name} - File already downloaded")
        return file_name
    # Download the file
    with open(os.path.join(directory, file_name), 'wb') as f:
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')
        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                print(f"\rDownloading {file_name}: [{'=' * done}{' ' * (50-done)}] {dl}/{total_length} bytes", end="", flush=True)
    print(f"\nDownloaded {file_name}")
    # Add the file name to the set of downloaded files
    downloaded_files.add(file_name)
    return file_name

# Function to extract zip files
def extract_zip(zip_file, extract_dir):
    # Extract into a subdirectory with the same name as the zip file (without the .zip extension)
    extract_subdir = os.path.splitext(os.path.basename(zip_file))[0]
    extract_path = os.path.join(extract_dir, extract_subdir)
    os.makedirs(extract_path, exist_ok=True)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print(f"Extracted {zip_file} to {extract_path}")

# Function to parse the webpage and find links
def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all links
    links = soup.find_all('a', href=True)
    total_files = 0
    downloaded_files_count = 0
    for link in links:
        href = link['href']
        # Check if the link starts with "/sites/default/files/election-data/"
        if href.startswith("/sites/default/files/election-data/"):
            # Prepend "https://www.sos.alabama.gov" to the href
            href = "https://www.sos.alabama.gov" + href
            # Download the file if it's not the download icon
            if "download-icon.svg" not in href:
                total_files += 1
                if href.endswith('.zip'):
                    file_name = download_file(href, "/home/linuxlaptop/Documents/AL_elections/data")
                    if file_name:
                        extract_zip(os.path.join("/home/linuxlaptop/Documents/AL_elections/data", file_name), "/home/linuxlaptop/Documents/AL_elections/data")
                        downloaded_files_count += 1
                elif href.endswith(('.pdf', '.xlsx', 'xls')):
                    file_name = download_file(href, "/home/linuxlaptop/Documents/AL_elections/data")
                    if file_name:
                        downloaded_files_count += 1
    print(f"\nTotal files found: {total_files}, Downloaded: {downloaded_files_count}")

if __name__ == "__main__":
    # Parse the webpage and download files
    parse_page(url)

