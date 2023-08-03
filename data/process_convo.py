import pandas as pd
import os


os.path.sep = "/"


def get_message_length(df_message: pd.DataFrame) -> pd.DataFrame:
    message_history = df_message


def get_engagement(df_message: pd.DataFrame) -> pd.DataFrame:
    df_engagement = (
        df_message.groupby("sender_name")
        .agg("count")
        .sort_values("content")
        .drop("timestamp_ms", axis="columns")
    )
    return df_engagement
