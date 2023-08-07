from data.utils.config import get_config
from data.utils.extract import get_convo_info
from data.process_convo import ConvoProcessor

# from data.utils.decoding import fix_encoding
import os
import glob
import argparse

os.path.sep = "/"


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config")
    return parser


def main():
    args = make_parser().parse_args()
    cfg = get_config(args.config)
    for conv_dir in glob.glob(os.path.join(cfg.input.path_to_data, "*")):
        convo_processor = ConvoProcessor(conv_dir, **cfg.input, **cfg.output)
        convo_processor.full_process_convo()


if __name__ == "__main__":
    main()
