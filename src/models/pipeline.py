from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import numpy as np

from src.features.text_features import (
    get_designation,
    get_description,
    first_words_series,
    numbers_units_series,
)

def build_pipeline(config):

    mode = config["mode"]

    max_features_word = config["model"][f"max_features_word_{mode}"]
    max_features_desc = config["model"][f"max_features_desc_{mode}"]
    max_iter = config["model"][f"max_iter_{mode}"]

    word_tfidf_designation = TfidfVectorizer(
        max_features=max_features_word,
        ngram_range=(1, 2),
        strip_accents="unicode",
        lowercase=True,
        sublinear_tf=True,
        min_df=5,
        max_df=0.8,
        dtype=np.float32,
    )

    word_tfidf_description = TfidfVectorizer(
        max_features=max_features_desc,
        ngram_range=(1, 2),
        strip_accents="unicode",
        lowercase=True,
        sublinear_tf=True,
        min_df=5,
        max_df=0.8,
        dtype=np.float32,
    )

    char_tfidf_designation = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        lowercase=True,
    )

    char_tfidf_description = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 6),
        min_df=3,
        lowercase=True,
    )

    features = ColumnTransformer(
        [
            ("designation_word",
             Pipeline([
                 ("select", FunctionTransformer(get_designation, validate=False)),
                 ("tfidf", word_tfidf_designation),
             ]),
             ["designation"]),

            ("designation_char",
             Pipeline([
                 ("select", FunctionTransformer(get_designation, validate=False)),
                 ("tfidf", char_tfidf_designation),
             ]),
             ["designation"]),

            ("description_word",
             Pipeline([
                 ("select", FunctionTransformer(get_description, validate=False)),
                 ("tfidf", word_tfidf_description),
             ]),
             ["description"]),

            ("description_char",
             Pipeline([
                 ("select", FunctionTransformer(get_description, validate=False)),
                 ("tfidf", char_tfidf_description),
             ]),
             ["description"]),

            ("first_words",
             Pipeline([
                 ("extract", FunctionTransformer(first_words_series, validate=False)),
                 ("tfidf", TfidfVectorizer()),
             ]),
             ["designation"]),

            ("numbers_units",
             Pipeline([
                 ("extract", FunctionTransformer(numbers_units_series, validate=False)),
                 ("tfidf", TfidfVectorizer()),
             ]),
             ["designation"]),
        ]
    )

    pipeline = Pipeline(
        [
            ("features", features),
            ("clf", LinearSVC(
                C=config["model"]["C"],
                class_weight="balanced",
                max_iter=max_iter,
                random_state=42,
            )),
        ]
    )

    return pipeline