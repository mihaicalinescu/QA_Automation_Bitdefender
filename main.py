import argparse
from sync_tool import FolderSyncer

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--source", required=True)
    parser.add_argument("--destination", required=True)
    parser.add_argument("--once", action="store_true")

    args = parser.parse_args()
    syncer = FolderSyncer(args.source, args.destination)

    if args.once:
        syncer.sync()

if __name__ == "__main__":
    main()