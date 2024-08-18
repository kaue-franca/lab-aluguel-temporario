import requests
import zipfile
import io
import os

def get_default_download_path():
    """
    Returns the default downloads path for the current user.
    """
    if os.name == 'nt':
        # Windows
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:
        # macOS and Linux
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    
def get_data(url):
    """
    Downloads data from a given URL.
    """

    download_path = get_default_download_path()

    try:
        response = requests.get(url)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(download_path)

            for file_name in zip_ref.namelist():
                if file_name.endswith('.csv'):
                    csv_filename = os.path.join(download_path, file_name)
                    break
        print(f"Saved as {csv_filename}")
        return csv_filename

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None