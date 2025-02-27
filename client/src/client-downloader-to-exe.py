import subprocess
import sys
from typing import List


def build_exe(script_path: str) -> None:
    """
    Compiles specified python script into .exe using PyInstaller.
    """
    command: List[str] = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--distpath", "target",
        "--workpath", "target/build",
        "--specpath", "target",
        script_path
    ]
    print(f"Running: {' '.join(command)}")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error during creation of exe:", e)
        sys.exit(1)

def main(file_name: str) -> None:
    print("Building executable...")
    build_exe(file_name)
    print("Finished!")


if __name__ == "__main__":
    main("client-downloader.py")
