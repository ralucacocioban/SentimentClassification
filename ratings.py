NEGATIVE = 1
POSITIVE = 2
MIXED = 3
OTHER = 4


def some(df, rating):
    """At least one of thar rating"""
    return df[
        (df["rating.1"] == rating) |
        (df["rating.2"] == rating) |
        (df["rating.3"] == rating) |
        (df["rating.4"] == rating) |
        (df["rating.5"] == rating) |
        (df["rating.6"] == rating) |
        (df["rating.7"] == rating) |
        (df["rating.8"] == rating)
    ]


def all(df, rating):
    """ Everyone with the same rating """
    return df[
        ((df["rating.1"] == rating) | (df["rating.1"] != df["rating.1"])) &
        ((df["rating.2"] == rating) | (df["rating.2"] != df["rating.2"])) &
        ((df["rating.3"] == rating) | (df["rating.3"] != df["rating.3"])) &
        ((df["rating.4"] == rating) | (df["rating.4"] != df["rating.4"])) &
        ((df["rating.5"] == rating) | (df["rating.5"] != df["rating.5"])) &
        ((df["rating.6"] == rating) | (df["rating.6"] != df["rating.6"])) &
        ((df["rating.7"] == rating) | (df["rating.7"] != df["rating.7"])) &
        ((df["rating.8"] == rating) | (df["rating.8"] != df["rating.8"]))
    ]
