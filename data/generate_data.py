import os
from dotenv import load_dotenv
import google.generativeai as genai
import re
from crawler import get_wikipedia_page_content
from json_util import get_path
import mwparserfromhell
import json
import google.generativeai as genai
import random
import csv

load_dotenv()
GEMINI_KEY = os.getenv('GEMINI_KEY')
LEN_THRESHOLD = 300

def get_paragraphs(s):
    blank_line_regex = r"(?:\r?\n){2,}"
    paragraph_list = re.split(blank_line_regex, s.strip())
    paragraph_list = [paragraph for paragraph in paragraph_list if len(paragraph) > LEN_THRESHOLD]
    return paragraph_list

def get_raw_text(content):
    raw_text = get_path(path=['query', 'pages'], data=content)
    raw_text = get_path(path=[list(raw_text.keys())[0], 'revisions', 0, 'slots', 'main', '*'], data=raw_text)
    return raw_text

def get_vie_text(page_title, language):
    content = get_wikipedia_page_content(page_title, language)
    vie_text = mwparserfromhell.parse(get_raw_text(content)).strip_code()
    return vie_text

def get_article_link(page_title, language):
    article_link = f"https://{language}.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
    return article_link

def paraphrase(paragraph):
    safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]
    model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
    genai.configure(api_key=GEMINI_KEY)
    response = model.generate_content(f"hãy viết 1 đoạn văn gần giống với : {paragraph}")
    return response.text

def save_to_csv(content, language, page_title):
    row = ['\n'.join(content), get_article_link(page_title=page_title, language=language)]
    filename = 'plagiarism.csv'
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row)

def generate_data_point(page_title, language):
    paragraph_list = get_paragraphs(get_vie_text(page_title=page_title, language=language))
    random_paragraphs = random.sample(paragraph_list, 4)
    content = [paraphrase(paragraph) for paragraph in random_paragraphs]
    save_to_csv(content=content, language=language, page_title=page_title)