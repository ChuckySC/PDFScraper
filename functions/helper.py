from functions.xml import xml_extract

def get_mapping(
    base: dict, 
    parameters: list, 
    max_rows: int, 
    request_form
) -> dict:
    for key in base.keys():
        for i in range(max_rows):
            fhw = {}
            for parametar in parameters:
                name = f'{key}-{parametar}-{i}'
                if name in request_form:
                    try:
                        fhw[parametar] = int(request_form[name])
                    except:
                        fhw[parametar] = None
                else:
                    fhw[parametar] = None
            base[key].append(fhw)
    return base

def get_structural_data(
    base: dict, 
    parameters: list, 
    max_rows: int, 
    request_form,
    file_path: str
) -> list:
    mapping = get_mapping(base, parameters, max_rows, request_form)
    return xml_extract(mapping, file_path)