import os
import sys
import requests
from typing import List, Dict, Any, Optional


def fetch_github_directory_contents(api_url: str) -> List[Dict[str, Any]]:
    """
    Fetches the contents of a directory from a given GitHub API URL.
    """
    try:
        response: requests.Response = requests.get(api_url)
        response.raise_for_status()
        contents: List[Dict[str, Any]] = response.json()
        return contents
    except requests.RequestException as e:
        print(f"Error during external file paths retrieval: {e}")
        sys.exit(1)


def download_file(download_url: str) -> bytes:
    """
    Downloads a file from the given URL.
    """
    try:
        response: requests.Response = requests.get(download_url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Failed to download file {download_url}: {e}")
        sys.exit(1)


def save_file(content: bytes, target_path: str) -> None:
    """
    Saves a file to a given target path.
    """
    try:
        with open(target_path, "wb") as f:
            f.write(content)
    except IOError as e:
        print(f"Failed to save file to {target_path}: {e}")
        sys.exit(1)

def ensure_minecraft_folder() -> str:
    """
    Returns the Minecraft folder on the current operating system.
    For Windows, it uses %APPDATA%\\.minecraft.
    For macOS, it uses ~/Library/Application Support/minecraft.
    For Linux, it uses ~/.minecraft.
    """
    if sys.platform == "darwin":  # macOS
        minecraft_folder = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "minecraft")
    elif sys.platform == "win32":  # Windows
        appdata: Optional[str] = os.getenv("APPDATA")
        if not appdata:
            print("Could not locate APPDATA env")
            sys.exit(1)
        minecraft_folder = os.path.join(appdata, ".minecraft")
    else:  # Assume Linux or other Unix-like systems
        minecraft_folder = os.path.join(os.path.expanduser("~"), ".minecraft")

    os.makedirs(minecraft_folder, exist_ok=True)
    return minecraft_folder


def download_directory(api_url: str, local_path: str) -> None:
    """
    Recursively downloads files and directories from the given GitHub API URL
    into the specified local path.
    """
    contents: List[Dict[str, Any]] = fetch_github_directory_contents(api_url)

    for item in contents:
        item_type = item.get("type")
        name = item.get("name", "")
        if item_type == "file":
            download_url: str = item.get("download_url", "")
            if download_url:
                target_file: str = os.path.join(local_path, name)

                if not os.path.exists(target_file):
                    print(f"Downloading new file: {name}...")
                    file_data: bytes = download_file(download_url)
                    save_file(file_data, target_file)
                else:
                    print(f"Skipping existing file: {name}")
        elif item_type == "dir":
            print(f"Entering directory: {name}...")
            new_local_folder: str = os.path.join(local_path, name)
            os.makedirs(new_local_folder, exist_ok=True)
            # Use the 'url' field to get the directory's contents
            new_api_url: str = item.get("url", "")
            if new_api_url:
                download_directory(new_api_url, new_local_folder)


def main(github_api_url: str) -> None:
    minecraft_folder: str = ensure_minecraft_folder()
    print(f"Downloading into {minecraft_folder}")
    download_directory(github_api_url, minecraft_folder)
    print("Finished!")


if __name__ == "__main__":
    main("https://api.github.com/repos/devformed/minecraft-server/contents/client/downloads")
