import pandas as pd
import os
from typing import Optional
from data.utils.decoding import fix_encoding
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import datetime
from plot.solar import show_polar
import glob
import json

os.path.sep = "/"

NOT_NAN_COLS_INDICATE_NOT_A_MESSAGE = {
    "is_unsent",
    "reactions",
    "sticker",
    "photos",
    "gifs",
}
HOURS_IN_A_DAY = 24


class ConvoProcessor:
    def __init__(
        self,
        convo_dir: str,
        output_data_path: str,
        supplementary_interactions: Optional[list[str]] = None,
        interactions_threshold: Optional[int] = None,
        encode: str = "latin-1",
        decode: str = "utf-8",
    ) -> None:
        self.convo_dir = convo_dir
        self.encode = encode
        self.decode = decode
        self.supplementary_interactions = supplementary_interactions
        self.interactions_threshold = interactions_threshold
        self.extract_convos_from_jsons()
        self.output_data_path = os.path.join(output_data_path, self.thread_path)

    def extract_convos_from_jsons(self):
        dfs_messages = []
        for jfile_path in glob.glob(os.path.join(self.convo_dir, "message_*.json")):
            # Retrieve contents
            with open(jfile_path, encoding="utf-8") as jfile:
                jfile.encoding
                contents = json.load(jfile)

            messages = contents["messages"]
            self.title = contents["title"].encode(self.encode).decode(self.decode)
            self.thread_path = os.path.basename(contents["thread_path"])
            df_messages_loc = pd.DataFrame(messages)
            df_messages_loc = fix_encoding(
                df_messages_loc,
                ["sender_name", "content"],
                encode=self.encode,
                decode=self.decode,
            )
            dfs_messages.append(df_messages_loc)

            participants = contents["participants"]
            df_participants = pd.DataFrame(participants)
            df_participants = fix_encoding(df_participants, ["name"])
        df_message = pd.concat(dfs_messages)
        df_message["timestamp"] = df_message["timestamp_ms"].apply(
            lambda tms: datetime.datetime.fromtimestamp(int(tms) * 1e-3)
        )
        df_message = df_message.drop("timestamp_ms", axis="columns")
        self.df_message = df_message

    def get_minimal_convo(self) -> pd.DataFrame:
        filtered_messages = self.df_message.copy()
        for col in NOT_NAN_COLS_INDICATE_NOT_A_MESSAGE.difference(set(self.supplementary_interactions or [])):
            if col in filtered_messages.columns:
                filtered_messages = filtered_messages[filtered_messages[col].isna()]

        return filtered_messages[["sender_name", "timestamp", "content"]]

    def get_engagement(self) -> pd.DataFrame:
        df_engagement = (
            self.df_message.groupby("sender_name")
            .agg("count")
            .sort_values("content")
            .drop("timestamp", axis="columns")
        )
        return df_engagement

    def get_length_histogram(self) -> pd.DataFrame:
        df_length = self.df_message.content.apply(len).value_counts()
        return df_length

    def save_artifact_df(self, df_to_save: pd.DataFrame, title) -> None:
        full_path = os.path.join(self.output_data_path, title)
        df_to_save.to_csv(full_path)

    def save_artifact_figure(self, figure: Figure, title) -> None:
        figure.tight_layout()
        figure.savefig(os.path.join(self.output_data_path, title))
        plt.cla()
        plt.clf()

    def get_timestamp_histogram_hours(self):
        df_messages = self.get_minimal_convo()
        hours: pd.Series = (
            df_messages["timestamp"]
            .dt.hour.value_counts()
            .sort_index()
            .reindex(list(range(0, HOURS_IN_A_DAY)), fill_value=0)
        )
        return hours

    def full_process_convo(self):
        df_engagement = self.get_engagement()
        if self.interactions_threshold is None or df_engagement.content.sum() > self.interactions_threshold:
            if not os.path.exists(self.output_data_path):
                os.makedirs(self.output_data_path)
            self.save_artifact_df(df_engagement, title="engagement")
            histogram = self.get_timestamp_histogram_hours()
            ax = show_polar(histogram, self.title)
            fig_hist = ax.get_figure()
            self.save_artifact_figure(fig_hist, "Histogram of the messages during the day")
