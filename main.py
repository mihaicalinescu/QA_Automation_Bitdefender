import argparse
import logging
from sync_tool import FolderSyncer


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("sync.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="One-way folder synchronization tool"
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Path to the source folder"
    )

    parser.add_argument(
        "--destination",
        required=True,
        help="Path to the destination folder"
    )

    parser.add_argument(
        "--once",
        action="store_true",
        help="Run synchronization only once"
    )

    return parser.parse_args()


def main():
    setup_logging()
    args = parse_arguments()

    logging.info("Application started")
    logging.info(f"Source folder: {args.source}")
    logging.info(f"Destination folder: {args.destination}")

    syncer = FolderSyncer(args.source, args.destination)

    if args.once:
        syncer.sync()
    else:
        logging.warning("No execution mode selected. Use --once for now.")

    logging.info("Application finished")


if __name__ == "__main__":
    main()