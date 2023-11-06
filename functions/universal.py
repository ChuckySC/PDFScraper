import json

def allowed_file(file_name, allowed_extensions):
    return (
        '.' in file_name and
        str(file_name).rsplit('.', 1)[1].lower() in allowed_extensions
    )
    
def load_xml(file):
    '''Load xml data'''
    with open(file, 'r', encoding='utf8') as f:
        data = f.read()
    return data

def load_json(file):
    '''Load json data'''
    with open(file, encoding='utf8') as input:
        data = json.load(input)
    return data

def save_json(data, file):
    '''Save json data into json file'''
    with open(file, 'w') as output:
        json.dump(data, output)