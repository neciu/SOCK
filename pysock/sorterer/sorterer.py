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


import os
from section import Section


def sort_critical_sections_in_pbx_file(pbx_file_path):
    raw_lines = read_raw_lines(pbx_file_path)

    sort_lines_in_section(section_key='PBXBuildFile', lines=raw_lines)
    sort_lines_in_section(section_key='PBXFrameworksBuildPhase', lines=raw_lines)
    sort_lines_in_section(section_key='PBXFileReference', lines=raw_lines)
    sort_lines_in_section(section_key='PBXGroup', lines=raw_lines)
    sort_lines_in_section(section_key='PBXResourcesBuildPhase', lines=raw_lines)
    sort_lines_in_section(section_key='PBXSourcesBuildPhase', lines=raw_lines)

    write_sorted_raw_lines(raw_lines, pbx_file_path)


def sort_lines_in_section(section_key, lines):
    section = Section(key=section_key, lines=lines)

    if section.start_line_index is None or section.end_line_index is None:
        AssertionError('Section %s does not contain starting or ending line index.' % section_key)

    section.records.sort(key=lambda x: x.name, reverse=False)

    for record in section.records:
        for line in record.property_lines:
            del lines[section.start_line_index + 1]

    line_index = section.start_line_index + 1
    for record in section.records:
        sort_deep_records_in_record(record)
        for line in record.property_lines:
            lines.insert(line_index, line)
            line_index += 1


def sort_deep_records_in_record(record):
    if record.deep_records is None:
        return
    record.deep_records.sort(key=lambda x: x.name, reverse=False)

    line_index = record.deep_record_start_line_index + 1
    for deep_record in record.deep_records:
        record.property_lines[line_index - record.start_line_index] = deep_record.content
        line_index += 1


def read_raw_lines(pbx_file_path):
    pbx_file = open(pbx_file_path, 'r')
    raw_lines = []
    for raw_line in pbx_file.read().splitlines():
        raw_lines.append(raw_line)
    pbx_file.close()
    return raw_lines


def write_sorted_raw_lines(raw_lines, pbx_file_path):
    os.remove(pbx_file_path)
    pbx_file = open(pbx_file_path, 'w')
    for line in raw_lines:
        pbx_file.write('%s\n' % line)
    pbx_file.close()
