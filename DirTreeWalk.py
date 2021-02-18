import os
import hashlib
import argparse

path_to_search = None

# total width of output
CONSOLE_WIDTH = 80
# number of spaces between table columns
NUMBER_OF_SPACES = 2

# calculate width for first and second column
print_width = int((CONSOLE_WIDTH - 32 - 2 * NUMBER_OF_SPACES) / 2)


def return_data_info(path):
    path_to_show = path + "/"

    global path_to_search
    if path_to_search is None:
        path_to_search = path

    print_path = path[len(path_to_search) + 1:]

    # append "/" for recursive runs
    if len(print_path) > 0:
        print_path = print_path + "/"

    try:
        with os.scandir(path) as p:
            for entry in p:
                # first process all regular files
                if entry.is_file() and entry.name[-4:] != ".lnk":
                    print_file_1st = entry.name
                    print_file_1st = check_and_adjust_length(print_file_1st)
                    print_file_2nd = print_path + entry.name
                    print_file_2nd = check_and_adjust_length(print_file_2nd)

                    #hash file with md5
                    filename = path_to_show + entry.name
                    buf_size = 65536  # 64kb bits
                    md5 = hashlib.md5()
                    try:
                        with open(filename, "rb") as f:
                            while True:
                                data = f.read(buf_size)
                                if not data:
                                    break
                                md5.update(data)
                    except PermissionError:
                        print(print_file_1st + NUMBER_OF_SPACES * " " + print_file_2nd)
                        print("...    -> " + entry.name + " :   Permission Error")
                        print("")

                    print_file_3rd = md5.hexdigest()

                    print(
                        print_file_1st + NUMBER_OF_SPACES * " " + print_file_2nd + NUMBER_OF_SPACES * " " + print_file_3rd)

        # second process all files marked with .lnk
        with os.scandir(path) as p:
            for entry in p:
                if entry.is_file() and entry.name[-4:] == ".lnk":
                    print_link_1st = entry.name
                    print_link_1st = check_and_adjust_length(print_link_1st)
                    print_link_2nd = "<link>"
                    print(print_link_1st + NUMBER_OF_SPACES * " " + print_link_2nd)

        # third process all regular directories
        with os.scandir(path) as p:
            for entry in p:
                if entry.is_dir():
                    print_dir_1st = entry.name
                    print_dir_1st = check_and_adjust_length(print_dir_1st)
                    print_dir_2nd = "<dir>"
                    print(print_dir_1st + NUMBER_OF_SPACES * " " + print_dir_2nd)

                    new_path = path + "/" + entry.name
                    # call recursive and start again
                    return_data_info(new_path)

    except PermissionError:
        print("...    -> " + print_path[:-1] + " :   Permission Error")
        print("")
    except FileNotFoundError:
        print("Error: Path not found: " + path)
    except Exception:
        print("there was an unexpected error")


def check_and_adjust_length(name):
    if len(name) > print_width:
        name = name[:print_width - 3] + "..."
    else:
        name = (name).ljust(print_width)
    return name


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to show")
    arg = parser.parse_args()
    return_data_info(arg.path)
