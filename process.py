from sys import argv
import os
from re import findall


INCLUDE_DIRECTIVE = '#include'
QUOTED_FLAG = '-q'
REPLACE_DICT_FLAG = '-r'
CURRENT_PATH = os.getcwd()

PROCESSED_STACK = []

ST_NORMAL = 0
ST_ACCUMULATE_DICT = 1
ST_REPLACE = 2

def print_help():
    _, script_name = os.path.split(argv[0])
    help_str = 'Simple script to process #include directive.\n\n\
Works both with relative and absolute paths:\n\
\t#include "test.txt"\n\
\t#include "../previous.ext"\n\
\t#include "X:/path/to/file.inc"\n\n\
Usage format:\n\n\
\tpython {}  <input_file_name>  <output_file_name>\n\n\
Run python {} -? to see this help.'.format(script_name, script_name)
    print(help_str)

def process_file(filepath):
    try:
        PROCESSED_STACK.append(filepath)
        file = open(filepath, 'r')
        input_lines = file.readlines()
        file.close()
        status = ST_NORMAL
        include_info = {}
        result = []
        i = 0
        while i < len(input_lines):
            line = input_lines[i]
            if status == ST_NORMAL:
                if line.strip().startswith(INCLUDE_DIRECTIVE):
                    include_info = parse_include(line)
                    include_path = include_info['path']
                    if not os.path.isfile(include_path):
                        current_dir, _ = os.path.split(filepath)
                        include_path = os.path.join(current_dir, include_path)
                        include_path = os.path.normpath(include_path)
                    if not include_path in PROCESSED_STACK:
                        include_info['lines'] = process_file(include_path)
                        PROCESSED_STACK.remove(include_path)
                    if include_info['has_replace_dict']:
                        status = ST_ACCUMULATE_DICT
                    i += 1
                else:
                    result.append(line)
                    i += 1
            elif status == ST_ACCUMULATE_DICT:
                if line.strip() == '}':
                    status = ST_REPLACE
                else:
                    key, value = parse_dict_record(line)
                    include_info['replace_dict'][key] = value
                i += 1
            elif status == ST_REPLACE:
                for key, value in include_info['replace_dict'].items():
                    for line in include_info['lines']:
                        result.append(line.replace(key, value))
                include_info.clear()
                status = ST_NORMAL
        if status != ST_NORMAL:
            raise EOFError('Unexpected end of file')
    except:
        print("Error processing file: " + filepath)
        raise
    if (len(result) > 0) and result[len(result)-1] != '\n':
        result.append('\n')
    return result

def parse_include(line):
    line = line.strip()
    start = line.find('"')
    if not start < 0:
        end = line.find('"', start+1)
        if not end < 0:
            path = line[start+1:end]
        else:
            raise ValueError('Incorrect include path parameter: quotes are not closed')
    else:
        raise ValueError('Include path parameter not found')
    params_list = parse_params(line[end:])
    result = {
        'path': get_path(path),
        'is_quoted': QUOTED_FLAG in params_list,
        'has_replace_dict': REPLACE_DICT_FLAG in params_list and line.endswith('{'),
        'lines': [],
        'replace_dict': {}
    }
    return result

def get_path(line):
    result = line.replace('/', os.sep)
    return result

def parse_params(params_str):
    return findall(r"\-[\w']", params_str)

def parse_dict_record(line):
    return '${db_name}', 'XXXX'

def write_result(output_filename, output):
    file = open(output_filename, 'w')
    file.writelines(output)
    file.close()

def process():
    input_path = argv[1]
    output_path = argv[2]
    try:
        if not os.path.isfile(input_path):
            input_path = os.path.join(CURRENT_PATH, input_path)
        result = process_file(input_path)
    except FileNotFoundError:
        print("Can't open input file")
    except:
        print("Can't process input file")
    else:
        try:
            output_path = get_path(output_path)
            if not os.path.isfile(output_path):
                output_path = os.path.normpath(os.path.join(CURRENT_PATH, output_path))
            write_result(output_path, result)
        except:
            print("Can't write output file")


if __name__ == "__main__":
    if len(argv) == 1 or '-?' in argv:
        print_help()
    elif len(argv) != 3:
        print("Bad arguments count. Expected 3, got {}\n".format(len(argv)))
        print_help()
    else:
        process()
