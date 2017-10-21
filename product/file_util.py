
def write_to_file(filename, document):
    f = open(filename, 'w')
    for line in document:
        f.write(line)
    f.close()

def write_line_to_file(filename, document):
    f = open(filename, 'w')
    for line in document:
        f.write(line+" ")
    f.close()

def read_from_file(filename):
    file = open(filename, 'r')
    # document = []
    # for line in file:
    #     document.append(line)
    data = file.read()
    return data

def read_list_from_file(filename):
    file = open(filename, 'r')
    document = []
    for line in file:
        document.append(line)
    return document

def append_to_file(filename, line):
    file = open(filename, 'a')
    file.write(line)