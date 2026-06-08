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

    # -----------------------------------------------------------------------
    # Bloc "pipeline" du config.yaml. Les .get(...) garantissent que si la
    # section est absente, on retombe EXACTEMENT sur le comportement historique.
    # -----------------------------------------------------------------------
    pipe_cfg = config.get("pipeline", {})
    lowercase = pipe_cfg.get("lowercase", True)

    feats = pipe_cfg.get("features", {})
    def enabled(name):
        return feats.get(name, True)

    char_cfg = pipe_cfg.get("char", {})
    char_desig = char_cfg.get("designation", {})
    char_descr = char_cfg.get("description", {})

    word_tfidf_designation = TfidfVectorizer(
        max_features=max_features_word,
        ngram_range=(1, 2),
        strip_accents="unicode",
        lowercase=lowercase,
        sublinear_tf=True,
        min_df=5,
        max_df=0.8,
        dtype=np.float32,
    )

    word_tfidf_description = TfidfVectorizer(
        max_features=max_features_desc,
        ngram_range=(1, 2),
        strip_accents="unicode",
        lowercase=lowercase,
        sublinear_tf=True,
        min_df=5,
        max_df=0.8,
        dtype=np.float32,
    )

    char_tfidf_designation = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(
            char_desig.get("ngram_min", 3),
            char_desig.get("ngram_max", 5),
        ),
        min_df=char_desig.get("min_df", 2),
        max_features=char_desig.get("max_features", None),
        lowercase=lowercase,
    )

    char_tfidf_description = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(
            char_descr.get("ngram_min", 3),
            char_descr.get("ngram_max", 6),
        ),
        min_df=char_descr.get("min_df", 3),
        max_features=char_descr.get("max_features", None),
        lowercase=lowercase,
    )

    # Construction conditionnelle des transformers (toggles config)
    transformers = []

    if enabled("designation_word"):
        transformers.append((
            "designation_word",
            Pipeline([
                ("select", FunctionTransformer(get_designation, validate=False)),
                ("tfidf", word_tfidf_designation),
            ]),
            ["designation"],
        ))

    if enabled("designation_char"):
        transformers.append((
            "designation_char",
            Pipeline([
                ("select", FunctionTransformer(get_designation, validate=False)),
                ("tfidf", char_tfidf_designation),
            ]),
            ["designation"],
        ))

    if enabled("description_word"):
        transformers.append((
            "description_word",
            Pipeline([
                ("select", FunctionTransformer(get_description, validate=False)),
                ("tfidf", word_tfidf_description),
            ]),
            ["description"],
        ))

    if enabled("description_char"):
        transformers.append((
            "description_char",
            Pipeline([
                ("select", FunctionTransformer(get_description, validate=False)),
                ("tfidf", char_tfidf_description),
            ]),
            ["description"],
        ))

    if enabled("first_words"):
        transformers.append((
            "first_words",
            Pipeline([
                ("extract", FunctionTransformer(first_words_series, validate=False)),
                ("tfidf", TfidfVectorizer(lowercase=lowercase)),
            ]),
            ["designation"],
        ))

    if enabled("numbers_units"):
        transformers.append((
            "numbers_units",
            Pipeline([
                ("extract", FunctionTransformer(numbers_units_series, validate=False)),
                ("tfidf", TfidfVectorizer(lowercase=lowercase)),
            ]),
            ["designation"],
        ))

    features = ColumnTransformer(transformers)

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