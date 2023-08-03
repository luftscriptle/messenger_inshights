import pandas as pd
import os
import glob
import json

os.path.sep = "/"


def fix_encoding(df, cols, encode: str = "latin-1", decode: str = "utf-8"):
    for col in cols:
        df.loc[:, col] = df[col].apply(lambda s: str(s).encode(encode).decode(decode))
    return df


def get_convo_info(convo_dir: str, encode: str = "latin-1", decode: str = "utf-8"):
    dfs_messages = []
    for jfile_path in glob.glob(os.path.join(convo_dir, "message_*.json")):
        # Retrieve contents
        with open(jfile_path, encoding="utf-8") as jfile:
            jfile.encoding
            contents = json.load(jfile)

        messages = contents["messages"]
        title = contents["title"].encode(encode).decode(decode)
        thread_path = os.path.basename(contents["thread_path"])
        df_messages_loc = pd.DataFrame(messages)
        df_messages_loc = fix_encoding(
            df_messages_loc, ["sender_name", "content"], encode=encode, decode=decode
        )
        dfs_messages.append(df_messages_loc)

        participants = contents["participants"]
        df_participants = pd.DataFrame(participants)
        df_participants = fix_encoding(df_participants, ["name"])
    df_message = pd.concat(dfs_messages)
    return df_message, title, thread_path


def get_engagement(df_message) -> pd.DataFrame:
    df_engagement = (
        df_message.groupby("sender_name")
        .agg("count")
        .sort_values("content")
        .drop("timestamp_ms", axis="columns")
    )
    return df_engagement
