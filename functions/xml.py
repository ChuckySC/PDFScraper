from functions.universal import load_xml
from models.abstract import Abstract

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

    return clean(txt_line), font, height, width

def skip(line: str, font: int, height: int, width: int, mapping: list) -> bool:
    results = []
    for el in mapping:
        if bool(el['font'] is None or el['font'] == font) and \
            bool(el['height'] is None or el['height'] == height) and \
                bool(el['width'] is None or el['width'] == width) and \
                    bool(el['line'] is None or el['line'] == line):
                        results.append(True)
        else:
            results.append(False)

    return all(results)

def xml_extract(mapping: dict, file_path: str) -> dict:
    abs_title = ''
    abs_content = ''
    abs_author = ''
    abs_page = ''

    root = load_xml(file_path)

    # first abstract
    #abstract = Abstract()
    
    for page in root.findall('page'):
        page_num = page.attrib['number']
        
        for line in page.findall('text'):
            txt_line, font, height, width = extract_from(line)
            
            if skip(txt_line, font, height, width, mapping['skip']):
                continue
            
    return