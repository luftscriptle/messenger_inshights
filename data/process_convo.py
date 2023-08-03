import pandas as pd
import os
from typing import Optional


os.path.sep = "/"

NOT_NAN_COLS_INDICATE_NOT_A_MESSAGE = {
    "is_unsent",
    "reactions",
    "sticker",
    "photos",
    "gifs",
}


def get_minimal_convo(
    df_message: pd.DataFrame, supplementary_interactions: Optional[list[str]] = None
) -> pd.DataFrame:
    filtered_messages = df_message.copy()
    for col in NOT_NAN_COLS_INDICATE_NOT_A_MESSAGE.difference(set(supplementary_interactions or [])):
        if col in filtered_messages.columns:
            filtered_messages = filtered_messages[filtered_messages[col].isna()]
    return filtered_messages[["sender_name", "timestamp_ms", "content"]]


def get_engagement(df_message: pd.DataFrame) -> pd.DataFrame:
    df_engagement = (
        df_message.groupby("sender_name")
        .agg("count")
        .sort_values("content")
        .drop("timestamp_ms", axis="columns")
    )
    return df_engagement


def get_length_histogram(df_message: pd.DataFrame):
    df_length = df_message.content.apply(len).value_counts()
    return df_length
