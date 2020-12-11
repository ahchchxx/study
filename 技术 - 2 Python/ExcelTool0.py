# -*- coding: utf-8 -*-
import base64
import datetime

import xlrd  # ==1.2.0
import xlwt  # ==1.3.0


DEFAULT_SERVER_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_SERVER_TIME_FORMAT = "%H:%M:%S"
DEFAULT_SERVER_DATETIME_FORMAT = "%s %s" % (
    DEFAULT_SERVER_DATE_FORMAT,
    DEFAULT_SERVER_TIME_FORMAT)

def read_excel(excel_file=None, is_base64=False):
    if is_base64:
        book = xlrd.open_workbook(file_contents=base64.b64decode(excel_file))
    else:
        book = xlrd.open_workbook(file_contents=excel_file)
    if len(book.sheets()) < 1:
        raise ('No sheet found.')
    # get worksheet
    sheet = book.sheet_by_index(0)
    assert sheet.nrows, 'The excel sheet should have at least 1 row'

    # get data
    row_titles = [cell.value for cell in sheet.row(0)]
    row_lines = []  # {}
    for i in range(1, sheet.nrows):
        values = []
        for cell in sheet.row(i):
            if cell.ctype is xlrd.XL_CELL_NUMBER:
                # is_float = cell.value % 1 != 0.0
                values.append(
                    cell.value  # str(cell.value)
                    # if is_float
                    # else str(int(cell.value))
                )
            elif cell.ctype is xlrd.XL_CELL_DATE:
                is_datetime = cell.value % 1 != 0.0
                # emulate xldate_as_datetime for pre-0.9.3
                dt = datetime.datetime(*xlrd.xldate.xldate_as_tuple(cell.value, book.datemode))
                values.append(
                    dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                    if is_datetime
                    else dt.strftime(DEFAULT_SERVER_DATE_FORMAT)
                )
            elif cell.ctype is xlrd.XL_CELL_BOOLEAN:
                values.append(u'True' if cell.value else u'False')
            elif cell.ctype is xlrd.XL_CELL_ERROR:
                raise ValueError(
                    "Invalid cell value at row %(row)s, column %(col)s: %(cell_value)s" % {
                        'row': i,  # rowx
                        'col': len(values) + 1, # cell.col,  # colx
                        'cell_value': xlrd.error_text_from_code.get(cell.value, "unknown error code %s" % cell.value)
                    }
                )
            else:
                values.append(cell.value)
        row_lines.append(values)

    return row_titles, row_lines


# def render_excel(self, model=None, method=None, record_id=None, context={}):
#     head_titles, body_lines, file_name = getattr(request.env[model], method)(record_id, context)
def render_excel(head_titles, body_lines, file_name):
    if ' ' in file_name:
        file_name = file_name.replace(' ', '%20')

    # 二、render excel
    # 1, create workbook
    workbook = xlwt.Workbook()
    bold = xlwt.easyxf("font: bold on;")  # style
    # 2, create worksheet
    worksheet = workbook.add_sheet('Sheet1')

    # 3, write data
    for index, data in enumerate(head_titles):
        worksheet.write(0, index, data, bold)
    for row_num, row_data in enumerate(body_lines, 1):
        for col, data in enumerate(row_data):
            worksheet.write(row_num, col, data)  # row_num start from 1

    # 4, response and close obj
    # response = request.make_response(
    #     None,  # excel_file,
    #     headers=[
    #         ('Content-Type', 'application/vnd.ms-excel'),
    #         ('Content-Disposition', "attachment; filename*=UTF-8''%s" % file_name)  # .xlsx
    #     ]
    # )
    # workbook.save(response.stream)
    # # workbook.close()
    #
    # return response

    # write to file
    workbook.save(file_name)


if __name__ == '__main__':
    # 1, write excel
    # head_titles = ['a', 'b', 'c']
    # body_lines = [[1, 2, 3], [5, 6, 8], ]
    # file_name = 'excel_test.xls'
    # render_excel(head_titles, body_lines, file_name)

    # 2, read excel
    with open('excel_test.xls', 'rb') as f:
        row_titles, row_lines = read_excel(base64.b64encode(f.read()))
        print(row_titles)
        # print(row_lines)
        for line in row_lines:
            print(line)

    pass
