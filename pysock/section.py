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


class SectionSection:
    def __init__(self, start_line_index, end_line_index, raw_lines):
        self.starting_line_index = start_line_index
        self.ending_line_index = end_line_index
        self.raw_lines = raw_lines
        self.lines = []

    def feed_lines(self):
        for i in range(self.starting_line_index - 1, self.ending_line_index):
            self.lines.append(Line(self.raw_lines[i]))

    def sort_lines(self):
        for line in self.lines:
            print line

        self.lines.sort(key=lambda x: x.content, reverse=False)

        for line in self.lines:
            print line

        for i in range(self.starting_line_index - 1, self.ending_line_index):
            self.raw_lines[i] = str(self.lines[i - self.starting_line_index])


def find_deep_sections(raw_lines):
    sections = []

    start_key = ' = ('
    end_key = ');'
    start_line_index = None
    end_line_index = None

    line_index = 1
    for raw_line in raw_lines:
        if start_key in raw_line:
            start_line_index = line_index + 1
        if end_key in raw_line:
            end_line_index = line_index - 1
            sections.append(
                SectionSection(start_line_index=start_line_index, end_line_index=end_line_index, raw_lines=raw_lines))
        line_index += 1

    return sections
