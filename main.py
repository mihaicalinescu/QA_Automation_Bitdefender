import argparse
import logging
import time
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

    mode_group = parser.add_mutually_exclusive_group(required=True)

    mode_group.add_argument(
        "--once",
        action="store_true",
        help="Run synchronization only once, immediately"
    )

    mode_group.add_argument(
        "--interval",
        help="Run synchronization periodically, e.g. 10s, 5m, 1h, 1d"
    )

    mode_group.add_argument(
        "--start-in",
        dest="start_in",
        help="Run one-time synchronization in the future, e.g. 30s, 5m, 1h, 1d"
    )

    return parser.parse_args()


def parse_interval(interval_str):
    if not interval_str:
        return None

    unit = interval_str[-1].lower()
    value = interval_str[:-1]

    if not value.isdigit():
        raise ValueError("Interval value must be a number followed by s, m, h, or d")

    value = int(value)

    if unit == "s":
        return value
    if unit == "m":
        return value * 60
    if unit == "h":
        return value * 3600
    if unit == "d":
        return value * 86400

    raise ValueError("Invalid interval unit. Use s, m, h, or d")


def main():
    setup_logging()
    args = parse_arguments()

    logging.info("Application started")
    logging.info(f"Source folder: {args.source}")
    logging.info(f"Destination folder: {args.destination}")

    syncer = FolderSyncer(args.source, args.destination)

    if args.once:
        logging.info("Running one-time synchronization immediately")
        syncer.sync()

    elif args.interval:
        interval_seconds = parse_interval(args.interval)
        logging.info(f"Running periodic synchronization every {args.interval}")

        while True:
            syncer.sync()
            logging.info(f"Waiting {interval_seconds} seconds until next synchronization")
            time.sleep(interval_seconds)

    elif args.start_in:
        delay_seconds = parse_interval(args.start_in)
        logging.info(f"One-time synchronization scheduled to start in {args.start_in}")
        time.sleep(delay_seconds)
        syncer.sync()

    else:
        logging.warning("No execution mode selected. Use --once, --interval or --start-in.")

    logging.info("Application finished")


if __name__ == "__main__":
    main()