from crawler import get_wikipedia_page_content
from json_util import fetch, get_path
import mwparserfromhell

def get_vie_text(page_title, language):
    content = get_wikipedia_page_content(page_title, language)
    raw_text = get_path(path=['query', 'pages', '777542', 'revisions', 0, 'slots', 'main', '*'], data=content)
    vi_text = mwparserfromhell.parse(raw_text).strip_code()
    return vi_text

# page_title = "Logarit"
# language = "vi"
# print(get_vie_text(page_title, language))
