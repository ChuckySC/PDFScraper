import json

def savejson(data, file):
    '''Save json data into json file'''
    with open(file, 'w') as output:
        json.dump(data, output)
        
def loadjson(file):
    with open(file) as input:
        data = json.load(input)
    return data