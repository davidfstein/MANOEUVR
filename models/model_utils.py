def get_fields(model):
    fields = []
    for item in vars(model).items():
        if item[0] == 'combined':
            continue
        fields.append(item[0])
    return fields

def get_field_vals(model):
    vals = []
    for item in vars(model).items():
        if item[0] == 'combined':
            continue
        vals.append(item[1])
    return vals

def print_attributes(model):
    print(', '.join("%s: %s" % item for item in vars(model).items()))