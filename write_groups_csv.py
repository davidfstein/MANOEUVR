import csv

def write_groups(groups):
    with open("groups.csv", "w+") as file:
        groupwriter = csv.writer(file)
        header_vals = get_header_vals(groups[0].subjects[0])
        header_vals.append("group number")
        groupwriter.writerow(header_vals)
        for i in range(len(groups)):
            for subject in groups[i].subjects:
                vals = get_subject_field_vals(subject)
                vals.append(i + 1)
                groupwriter.writerow(vals)

def get_header_vals(subject):
    header_vals = []
    for item in vars(subject).items():
        if item[0] == 'combined':
            continue
        header_vals.append(item[0])
    return header_vals

def get_subject_field_vals(subject):
    vals = []
    for item in vars(subject).items():
        if item[0] == 'combined':
            continue
        vals.append(item[1])
    return vals