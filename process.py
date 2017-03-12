from sys import argv
import os


INCLUDE_DIRECTIVE = "#include"
CURRENT_PATH = os.path.dirname(__file__)

def process_file(filename, base_path=CURRENT_PATH):
    try:
        filepath = os.path.join(base_path, filename)
        file = open(filepath, 'r')
        result = []
        for line in file:
            if line.strip().startswith(INCLUDE_DIRECTIVE):
                include_file_path = get_relpath(line)
                include_file_dir, include_file_name = os.path.split(include_file_path)
                next_base_path = os.path.join(base_path, include_file_dir)
                line = process_file(include_file_name, next_base_path)
                for x in line:
                    result.append(x)
            else:
                result.append(line)
        file.close()
    except:
        print("Error processing file: " + filepath)
    if (len(result) > 0) and result[len(result)-1] != '\n':
        result.append('\n')
    return result

def get_relpath(line):
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
            rel_path = get_relpath(output_name)
            output_path = os.path.normpath(os.path.join(CURRENT_PATH, rel_path))
            write_result(output_path, result)
        except:
            print("Can't write output file")
