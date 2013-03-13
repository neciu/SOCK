from pysock.section import find_deep_sections
from section import Section


def sort_critical_sections_in_pbx_file(pbx_file_path):
    pbx_file = open(pbx_file_path, 'r')

    raw_lines = []
    for raw_line in pbx_file.read().splitlines():
        raw_lines.append(raw_line)

    pbx_file.close()

    build_file_section = Section(key='PBXBuildFile', raw_lines=raw_lines)
    build_file_section.sort_lines()

    # for line in raw_lines:
    #     print line

    file_reference_section = Section(key='PBXFileReference', raw_lines=raw_lines)
    file_reference_section.sort_lines()

    # for line in raw_lines:
    #     print line

    # section1 = SectionWithThreeKeys(key='PBXGroup', key2='Resources', key3='children', raw_lines=raw_lines)
    # section1.sort_lines()
    #
    # section2 = SectionWithThreeKeys(key='PBXResourcesBuildPhase', key2='Resources', key3='files', raw_lines=raw_lines)
    # section2.sort_lines()

    deep_sections = find_deep_sections(raw_lines)
    for section in deep_sections:
        section.sort_lines()

    pbx_file = open(pbx_file_path, 'w')

    pbx_file.truncate()
    pbx_file.flush()
    pbx_file.write('')

    for line in raw_lines:
        pbx_file.write('%s\n' % line)

    pbx_file.close()

        # unsorted_file = open('unsorted', 'w')
        #
        # for line in build_file_section.lines:
        #     unsorted_file.write('%s\n' % line)
        # build_file_section.sort_lines()
        #
        # sorted_file = open('sorted', 'w')
        # for line in build_file_section.lines:
        #     sorted_file.write('%s\n' % line)




