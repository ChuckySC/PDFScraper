import xml.etree.ElementTree as ET
import json
import re

def allowed_file(file_name: str, allowed_extensions: list) -> bool:
    return (
        '.' in file_name and
        str(file_name).rsplit('.', 1)[1].lower() in allowed_extensions
    )

def load_xml(file_name: str):
    '''Load xml data'''
    tree = ET.parse(file_name)
    root = tree.getroot()
    return root
 
def load_xml_as_str(file_name: str) -> str:
    '''Load xml data'''
    with open(file_name, 'r', encoding='utf8') as f:
        data = f.read()
    return data

def load_json(file_name: str) -> json:
    '''Load json data'''
    with open(file_name, encoding='utf8') as input:
        data = json.load(input)
    return data

def save_json(data: json, file_name: str):
    '''Save json data into json file'''
    with open(file_name, 'w') as output:
        json.dump(data, output)
        
def remove_superscripts(text: str) -> str:
    text = re.sub(r'([a-z\xC0-\uFFFF])(\*|\d{1,2})(,|;|\s)',r'\g<1>\g<3>', text)
    text = re.sub(r',\d', ',', text)
    text = re.sub(r'(\d{1,2})([A-Z])',r'\g<1> \g<2>', text)
    text = re.sub(r'(MD|PhD|BS|RN|CRNI|FAAAAI|CME)\d', r'\g<1>', text)
    text = re.sub (r'\d,', ', ', text)
    text = re.sub(r',((\s+)?,)+', ',', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > 0 and text[-1] == ",":
        text = text[:-1]
    return text