import pandas as pd
import os
from typing import Optional
from data.utils.decoding import fix_encoding
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


class ConvoProcessor:
    def __init__(
        self,
        convo_dir: str,
        supplementary_interactions: list[str],
        encode: str = "latin-1",
        decode: str = "utf-8",
    ) -> None:
        self.convo_dir = convo_dir
        self.encode = encode
        self.decode = decode
        self.extract_convos_from_jsons()

    def extract_convos_from_jsons(self):
        dfs_messages = []
        for jfile_path in glob.glob(os.path.join(self.convo_dir, "message_*.json")):
            # Retrieve contents
            with open(jfile_path, encoding="utf-8") as jfile:
                jfile.encoding
                contents = json.load(jfile)

            messages = contents["messages"]
            title = contents["title"].encode(self.encode).decode(self.decode)
            thread_path = os.path.basename(contents["thread_path"])
            df_messages_loc = pd.DataFrame(messages)
            df_messages_loc = fix_encoding(
                df_messages_loc, ["sender_name", "content"], encode=self.encode, decode=self.decode
            )
            dfs_messages.append(df_messages_loc)

            participants = contents["participants"]
            df_participants = pd.DataFrame(participants)
            df_participants = fix_encoding(df_participants, ["name"])
        self.df_message = pd.concat(dfs_messages)

    def get_minimal_convo(
        self, df_message: pd.DataFrame, supplementary_interactions: Optional[list[str]] = None
    ) -> pd.DataFrame:

        filtered_messages = df_message.copy()
        for col in NOT_NAN_COLS_INDICATE_NOT_A_MESSAGE.difference(set(supplementary_interactions or [])):
            if col in filtered_messages.columns:
                filtered_messages = filtered_messages[filtered_messages[col].isna()]
        return filtered_messages[["sender_name", "timestamp_ms", "content"]]

    def get_engagement(self) -> pd.DataFrame:
        df_engagement = (
            self.df_message.groupby("sender_name")
            .agg("count")
            .sort_values("content")
            .drop("timestamp_ms", axis="columns")
        )
        return df_engagement

    def get_length_histogram(self) -> pd.DataFrame:
        df_length = self.df_message.content.apply(len).value_counts()
        return df_length
