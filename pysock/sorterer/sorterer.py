from section import Section, find_deep_sections


def sort_critical_sections_in_pbx_file(pbx_file_path):
    raw_lines = read_raw_lines(pbx_file_path)

    build_file_section = Section(key='PBXBuildFile', raw_lines=raw_lines)
    build_file_section.sort_lines()

    file_reference_section = Section(key='PBXFileReference', raw_lines=raw_lines)
    file_reference_section.sort_lines()

    group_section = Section(key='PBXGroup', raw_lines=raw_lines)

    deep_sections = find_deep_sections(raw_lines)
    for section in deep_sections:
        section.sort_lines()

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
