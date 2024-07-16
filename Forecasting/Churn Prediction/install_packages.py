import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def install_requirements(file_path='requirements.txt'):
    with open(file_path, 'r') as file:
        packages = file.readlines()
        packages = [package.strip() for package in packages]

    for package in packages:
        try:
            __import__(package.split('==')[0])
            print(f"{package} is already installed")
        except ImportError:
            print(f"Installing {package}")
            install(package)

if __name__ == "__main__":
    install_requirements()
