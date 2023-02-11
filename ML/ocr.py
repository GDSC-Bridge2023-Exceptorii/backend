import os, io
from google.cloud import vision
from google.cloud.vision_v1 import types
# from google.cloud import translate_v2 as translate
import pandas as pd
from google.oauth2 import service_account
import json

credential_path = "ServiceAccountToken.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def detect_text(path: str) -> str: 
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    df = pd.DataFrame(columns=['locale', 'description'])
    for text in texts:
        df = pd.concat([df, pd.DataFrame.from_records([dict(locale=text.locale, description=text.description)])], ignore_index=True)

    text: str = df['description'][0]

    return text
    
# df = pd.concat([df, pd.DataFrame.from_records
    
# if __name__ == "__main__":
#     print("OCR")
#     print(detect_text("ML/python_kor.jpg"))
#     print("Done")


from google.cloud import translate_v2
import pandas as pd
import json

def translate(text: str, target: str) -> str:
    trans_client = translate_v2.Client()
    detected_lang = trans_client.detect_language(text).get('language')
    translated = trans_client.translate(text, target_language=target)
    translated = translated.get('translatedText')
    return translated, detected_lang

# if __name__ == "__main__":
#     print("translate")
#     print(translate(detect_text("ML/python_kor.jpg")))
#     print("Done")


from transformers import PegasusForConditionalGeneration, PegasusTokenizer

def summarize(text: str) -> str:
    model_name = 'google/pegasus-xsum'
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    tokens = tokenizer([text], truncation=True, padding='longest', return_tensors="pt")
    summary = model.generate(**tokens)
    result = tokenizer.decode(summary[0])
    result = result.strip("<pad>")
    result = result.strip("</s>")

    return result

if __name__ == "__main__":
    print("summarize")
    text, lang = translate(detect_text("ML/python_kor.jpg"), "en")
    summary = summarize(text)
    print(summary)
    text_ori = translate(summary, lang)
    print(text_ori)
    print("Done")
