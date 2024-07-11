import os
import xlsxwriter
from django.core.files import File

from customer.models import StudentsExcel


def xlsx_writer(headers, data):
    directory = 'media/students'
    filename = f'{directory}/data.xlsx'

    if not os.path.exists(directory):
        os.makedirs(directory)

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    num = 1
    for row_num, student in enumerate(data, start=1):
        worksheet.write(row_num, 0, num)
        worksheet.write(row_num, 1, student.get("fullname"))
        worksheet.write(row_num, 2, student.get("phone_number"))
        worksheet.write(row_num, 3, student.get("parents"))
        worksheet.write(row_num, 4, student.get("coming"))
        worksheet.write(row_num, 5, student.get("school"))
        worksheet.write(row_num, 6, student.get("course"))
        worksheet.write(row_num, 7, student.get("group"))
        worksheet.write(row_num, 8, student.get("added_date"))
        worksheet.write(row_num, 9, student.get("grant"))
        worksheet.write(row_num, 10, student.get("balance"))
        worksheet.write(row_num, 11, student.get("status"))
        num += 1

    workbook.close()

    with open(filename, 'rb') as file:
        excel_file = File(file)
        excel_obj = StudentsExcel.objects.create(excel_file=excel_file)

    return excel_obj
