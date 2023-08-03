from data.utils.config import get_config
from data.utils.extract import get_convo_info
from data.process_convo import get_engagement, get_minimal_convo

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
        df_message, title, thread_path = get_convo_info(conv_dir)
        filtered_df = get_minimal_convo(
            df_message, supplementary_interactions=cfg.input.supplementary_interactions
        )
        # filtered_df = fix_encoding(filtered_df, cols=["content"])
        engagement_df = get_engagement(filtered_df)

        if engagement_df.content.sum() > cfg.input.interactions_threshold:
            filtered_df["messageLen"] = filtered_df.content.apply(len)
            longest_message = filtered_df[filtered_df.messageLen == filtered_df.messageLen.max()].content
            full_path = os.path.join(cfg.output.output_data_path, thread_path)
            print(f"For conversation '{title}', engagement: ")
            print(engagement_df)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            try:
                engagement_df.to_csv(os.path.join(full_path, "engagement.csv"))
            except OSError:
                print(f"Failed to save engagement in {title} convo")
            try:
                with open(os.path.join(full_path, "longest_message.txt").replace("\\", "/"), "w") as file:
                    file.writelines((longest_message))
            except (OSError, UnicodeEncodeError) as e:
                print(f"Failed to save longest message in {title} convo")


if __name__ == "__main__":
    main()
