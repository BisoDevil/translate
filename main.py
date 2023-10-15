from fastapi import FastAPI
from transformers import MarianMTModel, MarianTokenizer

app = FastAPI()


@app.get("/")
async def root():
    return "<h1>Hello</h1>"


@app.get("/translate")
async def say_hello(text: str):
    english_text = translate_arabic_to_english(text)
    return english_text


def translate_arabic_to_english(text):
    model_name = 'Helsinki-NLP/opus-mt-ar-en'
    # model_name = 'Helsinki-NLP/opus-mt-tc-big-en-it'
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # Tokenize the input text
    inputs = tokenizer.encode(text, return_tensors='pt')

    # Translate the input text
    translated = model.generate(inputs, max_length=1024, num_beams=4, early_stopping=True)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return {"data": translated_text}
