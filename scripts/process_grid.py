import sys
import os
from string import Template


def process_grid(path: str):
    ''' Function that write the classes for css grid

    The function require a css file with: 

        -   The columns and/or rows named in the "grid-template-columns" and/or
            the "grid-template-rows" propertys of the grid.

        -   A block to write the classes for the columns and another for the rows
            delimited for two comment lines:
                +   start:      /* ==== block [columns/rows] ==== */
                +   end:        /* ==== end block ==== */

    Note:   If there is code inside the block, the function will remplace all the
            content of the block.

    '''
    tmp_path = path + '.tmp'

    if not os.path.exists(path):
        raise FileNotFoundError('Css grid file not found')

    columns, rows = get_headers(path)

    insert_classes(path, columns, rows)

    os.remove(path)
    os.rename(tmp_path, path)


def get_headers(path: str):
    ''' Search the headers of the grid.

    Search the property grid-template-columns and grid-template-rows, then take the
    arguments and search for the arguments that start with "[" and ends with "]"

    '''
    with open(path, 'r') as file:
        columns = []
        rows = []

        line = file.readline()

        while line:
            # -2 to avoid the '\n' at the end of line
            keywords = line[:-2].split()

            if keywords:
                if keywords[0] == 'grid-template-columns:':
                    for k in keywords[1:]:
                        if (k[0] == '[' and k[-1] == ']'):
                            columns.append(k[1:-1])
                    print(columns)

                if keywords[0] == 'grid-template-rows:':
                    for k in keywords[1:]:
                        if (k[0] == '[' and k[-1] == ']'):
                            rows.append(k[1:-1])
                    print(rows)

            if columns != [] and rows != []:
                break

            line = file.readline()
        else:
            if columns == [] and rows == []:
                raise SyntaxError('No header detected')

    return columns, rows


def insert_classes(path: str, columns: list, rows: list):
    ''' Re-write the file

    Writes line by line the file in a temp file avoiding to write the content of the
    "block columns" and/or "block rows" and writing instead the classes created by
    the function.

    '''
    tmp_path = path + '.tmp'
    open(tmp_path, 'w').close()

    cols_block_id = '/* ==== block columns'
    rows_block_id = '/* ==== block rows'

    end_block_id = '/* ==== end block'

    with open(path, 'r') as file:
        line = file.readline()
        writing = True

        while line:
            if writing:
                with open(tmp_path, 'a') as tmp_file:
                    tmp_file.write(line)

            keywords = line[:-2].split()

            if ' '.join(keywords[:4]) == cols_block_id:
                writing = False
                if columns != []:
                    write_classes('column', columns, tmp_path)

            if ' '.join(keywords[:4]) == rows_block_id:
                writing = False
                if rows != []:
                    write_classes('row', rows, tmp_path, numeric_start=True)

            if ' '.join(keywords[:4]) == end_block_id and not writing:
                writing = True
            else:
                line = file.readline()

    return True


def write_classes(type: str, headers: list, path: str, numeric_start: bool = False):
    ''' Write the classes in the file

    Recive as arguments the type ["col"/"row"], the headers as a list, the path for
    the file and an optional argument to indicate if the headers name has an one
    character prefix used for names that starts with a number

    '''
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

        file.write('\n')


if __name__ == "__main__":
    process_grid(sys.argv[1])
