# -*- coding: utf-8 -*-
import base64
import datetime, json, copy
import io
from django.http import HttpResponse

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
        raise Exception('No sheet found.')
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

## some tips:
#   1, all of the sheet name should be static, using the same keyword
#   2， 起始行不是第一行的 sheet，约定开始的行数为： 第一个内容为“No.\n序号”所在的行
#   3， 末尾行不是业务所需数据的，某行的前两个cell为空的会被忽略掉！！！ 某行的第一个为“Sum\n合计”，第二个为空，会被忽略掉！！！
def read_excel_pn(excel_file=None, is_base64=False):
    if is_base64:
        book = xlrd.open_workbook(file_contents=base64.b64decode(excel_file))
    else:
        book = xlrd.open_workbook(file_contents=excel_file)
    if len(book.sheets()) < 1:
        raise Exception('No sheet found.')
    # return book.sheet_names()

    sheet_name_list = [
        {"name": '基本信息', 'is_first_row': True},  # Basic Info
        {"name": '计算结果', 'is_first_row': True},  # Calculate Result
        {"name": 'S-Payslip', 'is_first_row': False},
        {"name": 'S-Payroll Report', 'is_first_row': False},
        {"name": '工资税', 'is_first_row': True},  # IIT
        {"name": '年终奖税', 'is_first_row': True}, # Annual Bonus
    ]
    sheet_data_list = {'基本信息': {"row_titles": [], "row_lines": []},
                       '计算结果': {"row_titles": [], "row_lines": []},
                       'S-Payslip': {"row_titles": [], "row_lines": []},
                       'S-Payroll Report': {"row_titles": [], "row_lines": []},
                       '工资税': {"row_titles": [], "row_lines": []},
                       '年终奖税': {"row_titles": [], "row_lines": []},
                       }
    for cur_sheet in sheet_name_list:
        # get worksheet
        # sheet = book.sheet_by_index(0)
        sheet = book.sheet_by_name(cur_sheet["name"])
        assert sheet.nrows, 'The excel sheet should have at least 1 row'

        # parse to get start_row
        start_row = 0
        if not cur_sheet["is_first_row"]:
            for i in range(1, sheet.nrows):
                if sheet.row(i)[0].value == "No.\n序号":
                    start_row = i
                    break

            # get data
            # row_titles = [cell.value for cell in sheet.row(start_row)]
            row_titles = []
            for j in range(sheet.ncols):
                cell_val = sheet.cell(start_row + 1, j).value
                if not cell_val:
                    cell_val = sheet.cell(start_row, j).value
                row_titles.append(cell_val.strip())
            row_lines = []  # {}
            for i in range(start_row + 2, sheet.nrows):
                values = []
                j = -1
                for cell in sheet.row(i):
                    j += 1
                    ret_val = read_cell_value(cell, sheet_name=cur_sheet["name"], row_idx=i, col_idx=len(values) + 1, book=book)
                    values.append(ret_val)
                    if j == 2 and (values[0] == "" or values[0] == "Sum\n合计") and values[1] == "":
                        values = []
                        break  # ignore this row if first two are empty
                if values:
                    row_lines.append(values)
        else:
            # get data
            row_titles = [cell.value.strip() for cell in sheet.row(start_row)]
            row_lines = []  # {}
            for i in range(start_row + 1, sheet.nrows):
                values = []
                j = -1
                for cell in sheet.row(i):
                    j += 1
                    ret_val = read_cell_value(cell, sheet_name=cur_sheet["name"], row_idx=i, col_idx=len(values) + 1, book=book)
                    values.append(ret_val)
                    if j == 2 and values[0] == "" and values[1] == "":
                        values = []
                        break  # ignore this row if first two are empty
                if values:
                    row_lines.append(values)

        # return row_titles, row_lines
        sheet_data_list[cur_sheet["name"]]["row_titles"] = row_titles
        sheet_data_list[cur_sheet["name"]]["row_lines"] = row_lines

    return sheet_data_list

def read_cell_value(cell=None, sheet_name=None, row_idx=0, col_idx=0, book=None):
    ret_val = ""
    if cell.ctype is xlrd.XL_CELL_NUMBER:
        ret_val = cell.value
    elif cell.ctype is xlrd.XL_CELL_DATE:
        is_datetime = cell.value % 1 != 0.0
        # emulate xldate_as_datetime for pre-0.9.3
        dt = datetime.datetime(*xlrd.xldate.xldate_as_tuple(cell.value, book.datemode))
        if is_datetime:
            ret_val = dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        else:
            ret_val = dt.strftime(DEFAULT_SERVER_DATE_FORMAT)
    elif cell.ctype is xlrd.XL_CELL_BOOLEAN:
        ret_val = u'True' if cell.value else u'False'
    elif cell.ctype is xlrd.XL_CELL_ERROR:
        raise ValueError(
            "Invalid cell value at sheet %(sheet_name)s, row %(row)s, column %(col)s: %(cell_value)s" % {
                'sheet_name': sheet_name,
                'row': row_idx,  # rowx
                'col': col_idx,  # cell.col,  # colx
                'cell_value': xlrd.error_text_from_code.get(cell.value,
                                                            "unknown error code %s" % cell.value)
            }
        )
    else:
        ret_val = cell.value
    return ret_val


def render_excel(head_titles, body_lines, file_name,request):
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
    # workbook.close()

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename='+file_name

    # 写出到IO
    output = io.BytesIO()
    workbook.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())

    return response

    # write to file
    # workbook.save(file_name)


if __name__ == '__main__':
    # 1, write excel
    # head_titles = ['a', 'b', 'c']
    # body_lines = [[1, 2, 3], [5, 6, 8], ]
    # file_name = 'excel_test.xls'
    # render_excel(head_titles, body_lines, file_name)

    # 2, read excel
    # with open('excel_test.xls', 'rb') as f:
    #     row_titles, row_lines = read_excel(base64.b64encode(f.read()))
    #     print(row_titles)
    #     # print(row_lines)
    #     for line in row_lines:
    #         print(line)
    file_name = r'D:\Payslip Project - Doc\PN -AKOYABIO-202007.xlsx'
    with open(file_name, 'rb') as f:
        sheet_data_list = read_excel_pn(f.read(), is_base64=False)
        # print(sheet_data_list)
        for s_name, s_data in sheet_data_list.items():
            print(s_name)
            print(json.dumps(s_data))
            print("---------------------\n\n")


    pass
