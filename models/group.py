class Group():
    def __init__(self, subjects, num):
        self.subjects = subjects
        self.group_num = num
        self.combined_score = 0
    
    def set_group_num(self, num):
        self.group_num = num

    def add_subject(self, subject):
        self.subjects.append(subject)
        self.combined_score += subject.combined

    def __str__(self):
        return str([str(subject) for subject in self.subjects])