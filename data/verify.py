from generate_data import get_vie_text, get_paragraphs, get_article_link

FILE_NAME = 'articles_list.txt'
LANG = "vi"
LEFT = int(input("LEFT index: "))
RIGHT = int(input("RIGHT index: "))
MIN_PARAGRAPH_CNT = 4
INVALID = []

def check(title):
    vie_text = get_vie_text(page_title=title, language=LANG)
    if not vie_text:
        print('Unable to get page content')
        INVALID.append((title, 'Unable to get page content'))
        return False
    paragraphs = get_paragraphs(vie_text)
    if(len(paragraphs) < MIN_PARAGRAPH_CNT):
        print(f'Contains less than {MIN_PARAGRAPH_CNT} paragraphs')
        INVALID.append((title, f'# = {len(paragraphs)} paragraphs'))
        return False
    print(f'Contains {len(paragraphs)} paragraphs, verified successfully')
    return True

def verify(titles_list):
    for (index, title) in enumerate(titles_list):
        print(f'\n{index+LEFT} {title}')
        check(title=title)

with open(FILE_NAME, 'r', encoding='utf-8') as file:
    content = file.read().splitlines()[LEFT-1:RIGHT]
    verify(content)
    print('\nInvalid pages : ')
    for (title, verdict) in INVALID:
        print(f'{title} ({verdict}) : {get_article_link(page_title=title, language=LANG)}')
