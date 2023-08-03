from data.utils.config import get_config
from data.utils.extract import get_convo_info
from data.process_convo import get_engagement, get_message_length

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
        df_message, title, thread_path = get_convo_info(conv_dir)
        engagement_df = get_engagement(df_message)
        message_lens = get_message_lenghts(df_message)
        if engagement_df.content.sum() > 1500:
            full_path = os.path.join(cfg.output.output_data_path, thread_path)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            try:
                engagement_df.to_csv(os.path.join(full_path, "engagement.csv"))
            except OSError:
                print(f"Failed to save {title} convo")
            print(f"For conversation '{title}', engagement: ")
            print(engagement_df)


if __name__ == "__main__":
    main()
