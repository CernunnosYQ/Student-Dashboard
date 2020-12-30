import sys
import os
from string import Template


def process_grid(path):
    tmp_path = path + '.tmp'

    if not os.path.exists(path):
        raise FileNotFoundError('Css grid file not found')

    columns, rows = get_headers(path)

    insert_classes(path, columns, rows)

    os.remove(path)
    os.rename(tmp_path, path)


def insert_classes(path, columns, rows):
    tmp_path = path + '.tmp'
    open(tmp_path, 'w').close()

    cols_sec_id = '/* ==== Columns'
    rows_sec_id = '/* ==== Rows'

    with open(path, 'r') as file:
        line = file.readline()

        while line:
            with open(tmp_path, 'a') as tmp_file:
                tmp_file.write(line)

            clean_line = unindent_line(line)

            if clean_line[:len(cols_sec_id)] == cols_sec_id:
                if columns != []:
                    write_classes('column', columns, tmp_path)

            if clean_line[:len(rows_sec_id)] == rows_sec_id:
                if rows != []:
                    write_classes('row', rows, tmp_path, numeric_start=True)

            line = file.readline()

    return True


def write_classes(type, headers, path, numeric_start=False):
    tpl_start = Template(
        '\n.from-$suffix {\n  grid-$type-start: $header_name;\n}\n')
    tpl_end = Template('\n.to-$suffix {\n  grid-$type-end: $header_name;\n}\n')

    with open(path, 'a') as file:
        for h in headers:
            if numeric_start:
                suffix = h[1:]
            else:
                suffix = h

            if h != headers[-1]:
                file.write(tpl_start.substitute(
                    suffix=suffix, header_name=h, type=type))

            if h != headers[0]:
                file.write(tpl_end.substitute(
                    suffix=suffix, header_name=h, type=type))


def get_headers(path):
    with open(path, 'r') as file:
        line = file.readline()
        clean_line = ''

        columns = []
        rows = []

        while line:
            clean_line = unindent_line(line)

            if clean_line[:22] == 'grid-template-columns:':
                # -2 to avoid the '\n' at the end
                columns = extract_headers(clean_line[22:-2])
                print(columns)

            if clean_line[:19] == 'grid-template-rows:':
                # -2 to avoid the '\n' at the end
                rows = extract_headers(clean_line[19:-2])
                print(rows)

            if columns != [] and rows != []:
                break

            line = file.readline()
        else:
            if columns == [] and rows == []:
                raise SyntaxError('No header detected')

    return columns, rows


def extract_headers(line):
    headers_tmp = line.split()
    headers = []

    for h in headers_tmp:
        if h[0] == '[' and h[-1] == ']':
            headers.append(h[1:-1])

    return headers


def unindent_line(line):
    clean_line = ''
    for i in range(len(line)):
        if not (line[i] == ' '):
            clean_line = line[i:]
            break

    return clean_line


if __name__ == "__main__":
    process_grid(sys.argv[1])
