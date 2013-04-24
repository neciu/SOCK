# The MIT License (MIT)
#
# Copyright (c) 2013
#     Tomasz Netczuk (netczuk.tomasz at gmail.com)
#     Dariusz Seweryn (dariusz.seweryn at gmail.com)
#     https://github.com/neciu/SOCK
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


class DeepRecord():
    def __init__(self, content):
        self.content = content

        start_index = content.find('/*')
        end_index = content.find('*/')
        self.name = content[start_index + 2:end_index]


class Record():
    def __init__(self, lines, start_line_index):
        self.start_line_index = start_line_index
        self.end_line_index = self.find_end_line_index(lines)
        self.property_lines = self.load_attribute_lines(lines)
        self.name = self.find_record_name()
        self.deep_record_start_line_index = None
        self.deep_record_end_line_index = None
        self.deep_records = self.load_deep_records(lines)

    def find_end_line_index(self, lines):
        end_record_key = '};'

        line_index = 0
        while True:
            line = lines[self.start_line_index + line_index]
            if end_record_key in line:
                return self.start_line_index + line_index
            line_index += 1

        AssertionError('No end line index in record %s', str(self))

    def load_attribute_lines(self, lines):
        attribute_lines = []
        for line_index in range(0, self.end_line_index - self.start_line_index + 1):
            attribute_lines.append(lines[self.start_line_index + line_index])
        return attribute_lines

    def find_record_name(self):
        start_line = self.property_lines[0]
        key_start_index = start_line.find('/*')
        key_end_index = start_line.find('*/')
        return start_line[key_start_index + 2:key_end_index]

    def load_deep_records(self, lines):
        start_key = ' = ('
        end_key = ');'

        line_index = self.start_line_index
        for line in self.property_lines:
            if start_key in line:
                self.deep_record_start_line_index = line_index
            elif end_key in line:
                self.deep_record_end_line_index = line_index
            line_index += 1

        if self.deep_record_start_line_index is None or self.deep_record_end_line_index is None:
            return None

        deep_records = []
        for line_index in range(self.deep_record_start_line_index + 1, self.deep_record_end_line_index):
            deep_records.append(DeepRecord(lines[line_index]))

        return deep_records


class Section(object):
    def __init__(self, key, lines):
        self.key = key
        self.start_line_index = None
        self.end_line_index = None
        self.records = []

        self.find_start_and_end_line_indexes(lines)
        self.feed_records(lines)

    def find_start_and_end_line_indexes(self, lines):
        starting_line = '/* Begin %s section */' % self.key
        ending_line = '/* End %s section */' % self.key
        line_index = 0

        for line in lines:
            if starting_line in line:
                self.start_line_index = line_index
            if ending_line in line:
                self.end_line_index = line_index
                break
            line_index += 1

    def feed_records(self, lines):
        line_index = self.start_line_index + 1

        while (line_index < self.end_line_index):
            record = Record(lines, line_index)
            self.records.append(record)
            line_index += len(record.property_lines)


