from sys import argv
import os


INCLUDE_DIRECTIVE = "#include"
CURRENT_PATH = os.path.dirname(__file__)

def process_file(filename):
    filepath = os.path.join(CURRENT_PATH, filename)
    print(filepath)
    file = open(filepath, 'r')
    result = ''
    for line in file:
        if line.strip().startswith(INCLUDE_DIRECTIVE):
            include_file_path = get_include_relpath(line)
            line = process_file(include_file_path)
        result = result + line
    file.close()
    return result

def get_include_relpath(line):
    x = line.find('"')
    result = line[x:].replace('"', '').replace('\n', '').replace('/', os.sep)
    return result

def write_result(output_filename, result):
    file = open(output_filename, 'w')
    file.write(result)
    file.close()

if __name__ == "__main__":
    assert len(argv) == 3
    input_name = argv[1]
    output_name = argv[2]
    try:
        result = process_file(input_name)
    except FileNotFoundError:
        print("Can't open input file")
    except:
        print("Can't process input file")
    else:
        try:
            output_path = os.path.join(CURRENT_PATH, output_name)
            write_result(output_path, result)
        except:
            print("Can't write output file")
