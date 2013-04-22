import re


class Line():
    def __init__(self, raw_line):
        index = raw_line.find('/*')
        self.prefix = raw_line[:index]
        self.content = raw_line[index:]

        if self.prefix is not None or self.content is not None:
            prefix_in_right_format = re.compile('\\t*[A-Z0-9]{24} {1}').match(self.prefix)
            if not prefix_in_right_format:
                self.prefix = None
                self.content = None
        else:
            self.prefix = None
            self.content = None

    def __str__(self):
        if self.prefix is None or self.content is None:
            return 'Line with wrong prefix: "%s" or wrong content "%s".' % (self.prefix, self.content)
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
            line = Line(self.raw_lines[i])
            if line.prefix is not None and line.content is not None:
                self.lines.append(Line(self.raw_lines[i]))

    def sort_lines(self):
        self.lines.sort(key=lambda x: x.content, reverse=False)
        for i in range(self.starting_line_index - 1, self.ending_line_index):
            self.raw_lines[i] = str(self.lines[i - (self.starting_line_index - 1)])


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
            section = SectionSection(start_line_index=start_line_index, end_line_index=end_line_index, raw_lines=raw_lines)
            section.feed_lines()
            if len(section.lines) > 0:
                sections.append(section)
        line_index += 1

    return sections
