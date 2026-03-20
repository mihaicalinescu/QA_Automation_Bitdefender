from pathlib import Path
import shutil

class FolderSyncer:
    def __init__(self, source, destination):
        self.source = Path(source)
        self.destination = Path(destination)

    def sync(self):
        print("Starting sync...")
        self.copy_new_files()

    def copy_new_files(self):
        for item in self.source.iterdir():
            dest_path = self.destination / item.name

            if item.is_file():
                if not dest_path.exists():
                    shutil.copy2(item, dest_path)
                    print(f"Copied file: {item}")

            elif item.is_dir():
                    if not dest_path.exists():
                        dest_path.mkdir()
                        print(f"Created folder: {dest_path}")
