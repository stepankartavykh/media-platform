from dataclasses import dataclass
from pathlib import Path
from collections.abc import Callable

import yaml
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

config_path = Path(__file__).parent / "config.yaml"
with open(config_path, "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


@dataclass
class SentimentPrediction:
    """Class representing a sentiment prediction result."""

    label: str
    score: float


def load_bias_model() -> Callable[[str], SentimentPrediction]:
    tokenizer = AutoTokenizer.from_pretrained(config["sentiment_tokenizer"])
    model_ = AutoModelForSequenceClassification.from_pretrained(config["sentiment_model"])
    model_hf = pipeline(config["task"], model=model_, tokenizer=tokenizer)

    def model(text: str) -> SentimentPrediction:
        pred = model_hf(text)
        pred_best_class = pred[0]
        return SentimentPrediction(
            label=pred_best_class["label"],
            score=pred_best_class["score"],
        )

    return model
