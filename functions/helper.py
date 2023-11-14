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
                name = f'{key}-{parametar}-{i}' if 'select' not in parametar \
                                                else f'{key}-{parametar.replace("select-","")}-{i}-select'
                if name in request_form:
                    try:
                        if parametar == 'line' and str(request_form[name]) != '':
                            fhw[parametar] = str(request_form[name])
                        else:
                            fhw[parametar] = int(request_form[name])
                    except:
                        fhw[parametar] = None
                else:
                    fhw[parametar] = None

            is_empty = all([True if value is None else False for value in fhw.values()])
            if is_empty:
                continue

            base[key].append(fhw)
    return base

def get_structural_data(
    base: dict, 
    filters: dict,
    parameters: list, 
    max_rows: int, 
    request_form,
    file_path: str
) -> list:
    mapping = get_mapping(base, parameters, max_rows, request_form)
    return xml_extract(mapping, filters, file_path)