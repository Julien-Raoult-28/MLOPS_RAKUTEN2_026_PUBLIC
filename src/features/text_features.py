import re

UNIT_PATTERN = r"(cm|mm|m|kg|g|mg|l|ml|cl|w|kw|v|mah|ah|hz|ghz|mhz|go|gb|to|tb|mp|px|fps|°c|°)"

def get_designation(X):
    return X["designation"].fillna("").astype(str)

def get_description(X):
    return X["description"].fillna("").astype(str)

def first_words_series(X, n=3):
    return (
        X["designation"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.split()
        .str[:n]
        .str.join(" ")
    )

def numbers_units_series(X):
    return (
        X["designation"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.findall(rf"\b\d+[.,]?\d*\s?{UNIT_PATTERN}\b")
        .str.join(" ")
    )