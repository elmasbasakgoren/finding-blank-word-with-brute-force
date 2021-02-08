import time
import numpy as np

unwanted_chars = [",", ".", "'", "!", "\"", "?", "-", "(", ")"]


def _clean_inputs(data):
    data = data.lower()
    for _unwanted_char in unwanted_chars:
        data = data.replace(_unwanted_char, " ")
    while "  " in data:
        data = data.replace("  ", " ")
    return data.strip()


def _find(statement, raw_data_list):
    data_list = np.asarray(raw_data_list).reshape(-1, 1)
    statement_index_list = []
    for _point, _statement_piece in enumerate(statement):
        if _statement_piece.__eq__("___"):
            temp = statement_index_list[_point - 1]
            temp = list(map(lambda _val: _val + 1, temp))
            statement_index_list.append(np.asarray(temp))
            continue
        temp = np.where(data_list == _statement_piece)[0]
        statement_index_list.append(temp)
    statement_index_list = np.asarray(statement_index_list)

    founded_path_start_index = -1
    for _start_index in statement_index_list[0]:
        if _find_path(_start_index + 1, statement_index_list[1:]):
            founded_path_start_index = _start_index
            break

    text = ""
    for x in range(len(statement)):
        text += raw_data_list[founded_path_start_index + x] + " "
    return text[:-1]


def _find_path(check_index, statement_index_list):
    if statement_index_list.shape[0] == 1:
        if statement_index_list[0].tolist().__contains__(check_index):
            return True
        else:
            return False

    return statement_index_list[0].tolist().__contains__(check_index) and \
           _find_path(check_index + 1, statement_index_list[1:])


def start():
    with open("C:\\Users\\elmas\\OneDrive\\Masaüstü\\the_truman_show_script.txt") as _text_file:
        script_data = _clean_inputs(_text_file.read())
        script_data_list = script_data.split(" ")

    with open("C:\\Users\\elmas\\OneDrive\\Masaüstü\\statements.txt") as _text_file:
        statement_data = _text_file.read()
        statement_data_list = statement_data.splitlines()
        statement_data_list = list(map(
            lambda _dat: _clean_inputs(_dat).split(" "),
            statement_data_list))

    _start_time = time.time()
    for statement_line in statement_data_list:
        print(_find(statement_line, script_data_list))
    _end_time = time.time()

    print("\n\n\t\tTime table")
    print("Start time\t:", _start_time)
    print("End time\t:", _end_time)
    print("Difference\t:", (_end_time - _start_time))


if __name__ == '__main__':
    start()
