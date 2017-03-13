from sys import argv
import os


INCLUDE_DIRECTIVE = "#include"
CURRENT_PATH = os.getcwd()

PROCESSED_STACK = []

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
        result = []
        for line in file:
            if line.strip().startswith(INCLUDE_DIRECTIVE):
                include_file_path = parse_include(line)['path']
                if not os.path.isfile(include_file_path):
                    current_dir, _ = os.path.split(filepath)
                    include_file_path = os.path.join(current_dir, include_file_path)
                    include_file_path = os.path.normpath(include_file_path)
                if not include_file_path in PROCESSED_STACK:
                    line = process_file(include_file_path)
                    PROCESSED_STACK.remove(include_file_path)
                for line in line:
                    result.append(line)
            else:
                result.append(line)
        file.close()
    except:
        print("Error processing file: " + filepath)
        raise
    if (len(result) > 0) and result[len(result)-1] != '\n':
        result.append('\n')
    return result

def parse_include(line):
    start = line.find('"')
    if not start < 0:
        end = line.find('"', start+1)
        if not end < 0:
            path = line[start+1:end]
        else:
            raise ValueError('Incorrect include path parameter: quotes are not closed')
    else:
        raise ValueError('Include path parameter not found')
    result = {
        "path": get_path(path)
    }
    return result

def get_path(line):
    result = line.replace('/', os.sep)
    return result

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
