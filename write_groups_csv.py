from models import model_utils
import csv

def write_groups(groups):
    with open("groups.csv", "w+") as file:
        groupwriter = csv.writer(file)
        header_vals = model_utils.get_fields(groups[0].subjects[0])
        header_vals.append("group number")
        groupwriter.writerow(header_vals)
        for i in range(len(groups)):
            for subject in groups[i].subjects:
                vals = model_utils.get_field_vals(subject)
                vals.append(i + 1)
                groupwriter.writerow(vals)
            groupwriter.writerow("")
            groupwriter.writerow("")
            groupwriter.writerow("")

