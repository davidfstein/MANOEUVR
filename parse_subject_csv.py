import csv

def parse_subject_csv(path):
    with open(path, newline='', encoding="utf-8") as file:
        subjects = []
        reader = csv.reader(file)
        headers = next(reader)
        headers[0] = headers[0].strip('\ufeff')
        for line in reader:
            subject = dict(zip(headers, line))
            subjects.append(subject)
        return subjects

if __name__ == '__main__':
    s = parse_subject_csv('axolotl.csv')
    for d in s:
        print(d)