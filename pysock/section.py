class Line():
    def __init__(self, raw_line):
        index = raw_line.find('/*')
        self.prefix = raw_line[:index]
        self.content = raw_line[index:]

    def __unicode__(self):
        return self.prefix + self.content

    def __str__(self):
        return self.prefix + self.content


class Section(object):
    def __init__(self, key, raw_lines):
        self.key = key
        self.starting_line_number = None
        self.ending_line_number = None
        self.raw_lines = raw_lines
        self.lines = []

        self.find_starting_and_ending_line_number()
        self.feed_lines()

    def find_starting_and_ending_line_number(self):
        starting_line = '/* Begin %s section */' % self.key
        ending_line = '/* End %s section */' % self.key
        line_index = 1

        for raw_line in self.raw_lines:
            if starting_line in raw_line:
                self.starting_line_number = line_index + 1
            if ending_line in raw_line:
                self.ending_line_number = line_index - 1
                break
            line_index += 1

    def feed_lines(self):
        line_index = 1

        for raw_line in self.raw_lines:
            if line_index >= self.starting_line_number and line_index <= self.ending_line_number:
                self.lines.append(Line(raw_line))
            line_index += 1

    def sort_lines(self):
        if self.starting_line_number is None or self.ending_line_number is None:
            return

        self.lines.sort(key=lambda x: x.content, reverse=False)

        line_index = 1

        for raw_line in self.raw_lines:
            if line_index >= self.starting_line_number and line_index <= self.ending_line_number:
                self.raw_lines[line_index - 1] = str(self.lines[line_index - self.starting_line_number])
            line_index += 1

class SectionWithThreeKeys(Section):
    def __init__(self, key, key2, key3, raw_lines):
        self.key2 = key2
        self.key3 = key3
        super(SectionWithThreeKeys, self).__init__(key, raw_lines)


    def find_starting_and_ending_line_number(self):
        found_key_1 = False
        found_key_2 = False

        key_1_starting_line = '/* Begin %s section */' % self.key
        key_2_starting_line = '/* %s */ = {' % self.key2
        key_3_starting_line = '%s = ( = {' % self.key3
        key_3_ending_line = ');'

        line_index = 1

        for raw_line in self.raw_lines:
            if not found_key_1:
                if key_1_starting_line in raw_line:
                    found_key_1 = True
            if not found_key_2:
                if key_2_starting_line in raw_line:
                    found_key_2 = True
            if found_key_1 and found_key_2:
                if key_3_starting_line in raw_line:
                    self.starting_line_number = line_index + 1
                if key_3_ending_line in raw_line:
                    self.ending_line_number = line_index - 1
                    break

            line_index += 1


