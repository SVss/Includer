from sys import argv
import os


INCLUDE_DIRECTIVE = "#include"
CURRENT_PATH = os.getcwd()

PROCESSED_LIST = []

def process_file(filepath):
    try:
        PROCESSED_LIST.append(filepath)
        file = open(filepath, 'r')
        result = []
        for line in file:
            if line.strip().startswith(INCLUDE_DIRECTIVE):
                include_file_path = get_path(line)
                if not os.path.isfile(include_file_path):
                    current_dir, _ = os.path.split(filepath)
                    include_file_path = os.path.join(current_dir, include_file_path)
                    include_file_path = os.path.normpath(include_file_path)
                if not include_file_path in PROCESSED_LIST:
                    line = process_file(include_file_path)
                for line in line:
                    result.append(line)
            else:
                result.append(line)
        file.close()
    except:
        print("Error processing file: " + filepath)
    if (len(result) > 0) and result[len(result)-1] != '\n':
        result.append('\n')
    return result

def get_path(line):
    x = line.find('"')
    if (x > 0):
        line = line[x:]
    result = line.rstrip('\n').strip('"').replace('/', os.sep)
    return result

def write_result(output_filename, output):
    file = open(output_filename, 'w')
    file.writelines(output)
    file.close()

if __name__ == "__main__":
    assert len(argv) == 3
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
