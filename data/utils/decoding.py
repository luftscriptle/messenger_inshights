def fix_encoding(df, cols, encode: str = "latin-1", decode: str = "utf-8"):
    for col in cols:
        df.loc[:, col] = df[col].apply(lambda s: str(s).encode(encode).decode(decode))
    return df
