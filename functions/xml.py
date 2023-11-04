def clean(line: str) -> str:
    return line.replace('\u2800', '').strip()
    
def extract(txtline):
    '''Get elements from xml text tag'''
    
    height = int(txtline.attrib['height'])
    font = int(txtline.attrib['font'])
    width = int(txtline.attrib['width'])
    if txtline.text: 
        line = txtline.text
    else:
        line = ''
        for part in txtline.itertext():
            line = line + part
    return clean(line), font, height, width