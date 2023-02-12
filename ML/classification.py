# TODO: classify news summaries using ML: Huggingface BERT.
import math
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-dec2021-tweet-topic-multi-all")

model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-dec2021-tweet-topic-multi-all")

def classify(text: str) -> str:
    """Classify news summaries using ML: Huggingface BERT."""
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    prediction = logits.argmax()
    return prediction

if __name__ == "__main__":
    test_1 = "The advancement of AI is too fast and we need to be careful."
    test_2 = "Hackathons are fun: here's five reasons why."
    test_3 = "The new iPhone 12 is out and it's the best phone ever."
    test_4 = "Scammers are using the pandemic to steal your money."

    print(classify(test_1))
    print(classify(test_2))
    print(classify(test_3))
    print(classify(test_4))