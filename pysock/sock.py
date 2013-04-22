import sys
from sorterer.sorterer import sort_critical_sections_in_pbx_file

def main(arguments):
    if not len(arguments) == 2:
        print 'Error: wrong number of arguments.'
    else:
        pbx_file_path = arguments[1]
        sort_critical_sections_in_pbx_file(pbx_file_path)

if __name__ == "__main__":
    main(sys.argv)