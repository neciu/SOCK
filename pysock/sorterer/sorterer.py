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


from section import Section


def sort_critical_sections_in_pbx_file(pbx_file_path):
    raw_lines = read_raw_lines(pbx_file_path)

    build_file_section = Section(key='PBXBuildFile', raw_lines=raw_lines)
    raw_lines = build_file_section.sort_lines()

    file_reference_section = Section(key='PBXFileReference', raw_lines=raw_lines)
    raw_lines = file_reference_section.sort_lines()

    group_section = Section(key='PBXGroup', raw_lines=raw_lines)
    raw_lines = group_section.sort_lines()

    resources_section = Section(key='PBXResourcesBuildPhase', raw_lines=raw_lines)
    raw_lines = resources_section.sort_lines()

    sources_section = Section(key='PBXSourcesBuildPhase', raw_lines=raw_lines)
    raw_lines = sources_section.sort_lines()

    write_sorted_raw_lines(raw_lines, pbx_file_path)


def read_raw_lines(pbx_file_path):
    pbx_file = open(pbx_file_path, 'r')
    raw_lines = []
    for raw_line in pbx_file.read().splitlines():
        raw_lines.append(raw_line)
    pbx_file.close()
    return raw_lines


def write_sorted_raw_lines(raw_lines, pbx_file_path):
    pbx_file = open(pbx_file_path, 'w')
    pbx_file.truncate()
    pbx_file.flush()
    pbx_file.write('')
    for line in raw_lines:
        pbx_file.write('%s\n' % line)
    pbx_file.close()
