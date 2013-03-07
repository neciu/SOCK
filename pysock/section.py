class Section:
    def __init__(self, name, key, pbx_file):
        self.name = name
        self.key = key
        self.pbx_file = pbx_file
        self.starting_line_number = None
        self.ending_line_number = None
        self.indentation = None
        self.lines = []

