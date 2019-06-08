
def Subject():
    return type('Subject', (), {'__init__': subject_init})

def subject_init(self, attributes):
    combined = 0
    for attr, value in attributes.items():
        if attr != "id":
            combined += float(value)
        setattr(self, attr, float(value))
    self.combined = combined