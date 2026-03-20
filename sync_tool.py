from pathlib import Path
import shutil


class FolderSyncer:
    def __init__(self, source, destination):
        self.source = Path(source)
        self.destination = Path(destination)

    def sync(self):
        print("Starting sync...")

        if not self.source.exists():
            raise ValueError("Source folder does not exist")

        if not self.destination.exists():
            self.destination.mkdir(parents=True)

        self._sync_source_to_destination(self.source, self.destination)
        self._delete_extra_items(self.source, self.destination)

    def _sync_source_to_destination(self, source_dir, destination_dir):
        for item in source_dir.iterdir():
            dest_path = destination_dir / item.name

            if item.is_dir():
                if not dest_path.exists():
                    dest_path.mkdir()
                    print(f"Created folder: {dest_path}")

                self._sync_source_to_destination(item, dest_path)

            elif item.is_file():
                if not dest_path.exists():
                    shutil.copy2(item, dest_path)
                    print(f"Copied new file: {item} -> {dest_path}")
                else:
                    if self._files_are_different(item, dest_path):
                        shutil.copy2(item, dest_path)
                        print(f"Updated file: {item} -> {dest_path}")

    def _delete_extra_items(self, source_dir, destination_dir):
        for item in destination_dir.iterdir():
            source_path = source_dir / item.name

            if not source_path.exists():
                if item.is_file():
                    item.unlink()
                    print(f"Deleted extra file: {item}")
                elif item.is_dir():
                    shutil.rmtree(item)
                    print(f"Deleted extra folder: {item}")
            else:
                if item.is_dir() and source_path.is_dir():
                    self._delete_extra_items(source_path, item)

    def _files_are_different(self, source_file, destination_file):
        return (
            source_file.stat().st_size != destination_file.stat().st_size
            or source_file.read_bytes() != destination_file.read_bytes()
        )