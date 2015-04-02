def minus_df(df):
    """Extract all the tweets with -"""
    return df[df["content"].str.contains("[^0-9]\-[0-9]+")]


def plus_df(df):
    """Extract all the tweets with +"""
    return df[df["content"].str.contains("\+[0-9]+")]


def happy_df(df):
    return df[df["content"].str.contains("[:;8=xX]-?[\)\]D]")]


def sad_df(df):
    return df[df["content"].str.contains("[:;8=]'?-?[\(\[\|]")]
