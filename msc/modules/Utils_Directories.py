import os


def createDirectory(dirPath):
    """Creates a directory if it does not exist."""
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
        print(f"\nDirectory created: {dirPath}")
    else:
        print(f"\nDirectory already exists: {dirPath}")
