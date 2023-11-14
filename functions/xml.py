from functions.universal import load_xml
from models.abstract import Abstract

ABS_EXCEPTIONS = [    
    'background',
    'backgroud',
    '<background>',
    'conclusion',
    'objective',
    'acknowledgements',
    'introduction',
    '(introduction)',
    'intro',
    'goals',
    'importance',
    'summary',
    'methods',
    'purpose',
    '[purpose]',
    'keywords',
    '1. background and aim',
    'aim',
    'abstract background',
    'abstract',
    'rational',
    'significance'
]

def clean(line: str) -> str:
    return line.replace('\u2800', '').strip()

def extract_from(line):
    '''Get elements from xml text tag'''
    
    height = int(line.attrib['height'])
    font = int(line.attrib['font'])
    width = int(line.attrib['width'])

    if line.text:
        txt_line = line.text
    else:
        txt_line = ''
        for part in line.itertext():
            txt_line = txt_line + part

    return clean(txt_line), width, height, font

def is_true(line: str, width: int, height: int, font: int, mapping: list, filters: dict) -> bool:
    if not bool(mapping):
        # Returns False if mapping length is 0
        # i.e. equivalent to -> if len(mapping) == 0
        return False

    for el in mapping:
        is_width = False
        is_height = False
        is_font = False
        is_line = False
        
        is_width = bool(el['width'] is None or el['width'] == width) \
            if el['select-width'] == filters['equal_to'] \
            else bool(el['width'] is None or el['width'] > width) \
                if el['select-width'] == filters['greater_than'] \
                else bool(el['width'] is None or el['width'] < width)

        is_height = bool(el['height'] is None or el['height'] == height) \
            if el['select-height'] == filters['equal_to'] \
            else bool(el['height'] is None or el['height'] > height) \
                if el['select-height'] == filters['greater_than'] \
                else bool(el['height'] is None or el['height'] < height)

        is_font = bool(el['font'] is None or el['font'] == font) \
            if el['select-font'] == filters['equal_to'] \
            else bool(el['font'] is None or el['font'] > font) \
                if el['select-font'] == filters['greater_than'] \
                else bool(el['font'] is None or el['font'] < font)

        is_line = bool(el['line'] is None or el['line'] == line) \
            if el['select-line'] == filters['equal_to'] \
            else bool(el['line'] is None or el['line'] > line) \
                if el['select-line'] == filters['starts_with'] \
                else bool(el['line'] is None or line.startswith(el['line']))

        if bool(is_width and is_height and is_font and is_line):
            return True

    return False

def is_exception(line: str, exceptions: list) -> bool:
    for exception in exceptions:
        if line.startswith(exception):
            return True

    return False

def xml_extract(mapping: dict, filters: dict, file_path: str) -> list:
    ### SET LOCAL PARAMETERS
    abstracts = []
    abs = None

    abs_title = ''
    abs_content = ''
    abs_author = ''
    abs_page = ''

    # is_title_started = False
    is_author_started = False
    is_abs_started = False

    ### LOAD XML DATA
    root = load_xml(file_path)

    ### PROCESS EACH LINE
    for page in root.findall('page'):
        page_num = page.attrib['number']

        for line in page.findall('text'):
            txt_line, width, height, font = extract_from(line)

            if is_exception(txt_line.lower(), ABS_EXCEPTIONS):
                is_abs_started = True

            if (
                clean(txt_line) == '' or
                is_true(txt_line, width, height, font, mapping['skip'], filters)
            ):
                continue

            # ABS TITLE
            if (
                is_true(txt_line, width, height, font, mapping['title'], filters)
                or is_true(txt_line, width, height, font, mapping['title-start'], filters)
            ):
                if abs_title == '':
                    abs_page = page_num
                abs_title = f'{abs_title} {txt_line}'.strip() if abs_title != ''  else txt_line.strip()
                is_author_started = True
                continue

            # ABS AUTHOR(S)
            if (
                is_true(txt_line, width, height, font, mapping['author'], filters) 
                or is_true(txt_line, width, height, font, mapping['author-start'], filters)
            ) and is_author_started and not is_abs_started:
                abs_author = f'{abs_author} {txt_line}'.strip() if abs_author != ''  else txt_line.strip()
                # is_title_started = False
                continue

            # NEW ABS STARTS
            if (
                is_true(txt_line, width, height, font, mapping['content'], filters)
                or is_true(txt_line, width, height, font, mapping['content-start'], filters)
            ) and is_abs_started and is_author_started:
                # is_title_started = False
                is_author_started = False

                if abs:
                    # Add previous abstract
                    abs.content = abs_content
                    abstracts.append(abs.get())

                # Call class constructor    
                abs = Abstract(
                    title=abs_title,
                    author=abs_author,
                    page=abs_page
                )

                # Clear variables
                abs_title = ''
                abs_content = ''
                abs_author = ''
                abs_page = ''

                abs_content = txt_line.strip()
                continue

            # ELSE abs content
            if is_abs_started:
                abs_content = f"{abs_content} {txt_line}".strip()

    # Add last abstract
    if abs:
        abs.content = abs_content
        abstracts.append(abs.get())   

    ### RETURN STRUCTURED LIST OF DATA
    return abstracts