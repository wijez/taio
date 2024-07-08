import os
import re
import shutil
import time

import pandas as pd

from constant import taio_constant
from settings import Settings
import fitz
from datetime import datetime

settings = Settings()
df = pd.read_csv(settings.excel_link)
pdf_directory = settings.download_directory
excel_tax_codes = df['Mã số thuế bên bán'].tolist()


def open_pdf_file(pdf_file_path):
    pdf_document = fitz.open(pdf_file_path)
    full_text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        page_text = page.get_text()
        full_text += page_text
    pdf_document.close()
    return full_text


def extract_tax_info_from_pdf(full_text):
    patterns = [
        r"Tên người bán:\s*(.*)\nMã số thuế:\s*(\d+)\s*",
        r"Tên người bán:\s*(.*)\nMã số thuế:\s*((?:\d\s*)+)\s*",
        r"Đơn vị bán hàng:\s*(.*)\nMã số thuế:\s*((?:\d\s*)+)\s*",
        # r"""
        #     Đơn vị bán hàng \(Seller\):\s*\n
        #     Mã số thuế \(Tax code\):\s*\n
        #     (?:.*\n)*?
        #     (?P<company_name>.+)\n
        #     (?P<tax_code>(?:\d\s*)+)
        # """,
        # r"CÔNG TY [A-ZĐĂÂƠƯÊÔÀẢÃÁẠĂẰẲẴẶÂẦẨẪẬÈẺẼÉẸÊỀỂỄỆÌỈĨÍỊÒỎÕÓỌÔỒỔỖỘƠỜỞỠỢÙỦŨÚỤƯỪỬỮỰỲỶỸÝỴ\s]+Mã số thuế:\s*(\d+)",
        # r"Đơn vị bán hàng \(Seller\):\s*(.+)\nMã số thuế \(Tax code\):\s*([\d\s]+)",
        # r"Số \(No.\):\s*(\d+)\s+CÔNG TY TNHH ["
        # r"A-ZĐĂÂƠƯÊÔÀẢÃÁẠĂẰẲẴẶÂẦẨẪẬÈẺẼÉẸÊỀỂỄỆÌỈĨÍỊÒỎÕÓỌÔỒỔỖỘƠỜỞỠỢÙỦŨÚỤƯỪỬỮỰỲỶỸÝỴ\s]+\nMã số thuế \(Tax code\):\s*(["
        # r"\d\s]+)",
        # r"(\d{10}|\d{13})\s*:\s*\(Tax code\)\s*Mã số thuế\s*(.*?)\s*:\s*\(Seller\)\s*Đơn vị bán hàng",
        # r'Mã số thuế \(Tax code\):\s*([\d\s]+)\s*CÔNG\s*TY\s*CỔ\s*PHẦN\s*(['
        # r'A-ZĐĂÂƠƯÊÔÀẢÃÁẠĂẰẲẴẶÂẦẨẪẬÈẺẼÉẸÊỀỂỄỆÌỈĨÍỊÒỎÕÓỌÔỒỔỖỘƠỜỞỠỢÙỦŨÚỤƯỪỬỮỰỲỶỸÝỴ\s]*)\s*(?:\n|$)',
    ]

    pdf_tax_dict = {}
    for pattern in patterns:
        matches = re.findall(pattern, full_text, re.MULTILINE)
        print(f"Pattern: {pattern}, Matches: {matches}")
        if matches:
            for match in matches:
                pdf_tax_dict[match[1]] = match[0]
            break

    return pdf_tax_dict


def check_tax_code_in_excel(tax_code, excel_tax_codes):
    return tax_code in excel_tax_codes


def add_row(df, new_data):
    new_row = pd.Series(new_data, index=df.columns)
    df = df._append(new_row, ignore_index=True)
    # df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
    # df = pd.concat([df.dropna(how='all'), new_row.dropna()], ignore_index=True)
    return df

new_data_template = {
    'No': '',
    'Link': '',
    'Bên bán': '',
    'Mã số thuế bên bán': '',
}


def update_row(df, pdf_tax_dict, excel_tax_codes, pdf_file_path):
    updated = False
    df_copy = df.copy()
    for tax_code, seller_name in pdf_tax_dict.items():
        if not check_tax_code_in_excel(tax_code, excel_tax_codes):
            print(f"There is no tax code {tax_code} in the Excel file, please add a new one...")
            new_data = new_data_template.copy()
            new_data['No'] =  len(df_copy) + 1
            new_data['Link'] = pdf_file_path
            new_data['Bên bán'] = seller_name
            new_data['Mã số thuế bên bán'] = tax_code

            df = add_row(df, new_data)
            excel_tax_codes.append(tax_code)
            updated = True

    if updated:
        df.to_csv(settings.excel_link, index=False)
        print("File Excel updated.")
    else:
        print("There are no changes in the file Excel.")


for pdf_file_name in os.listdir(pdf_directory):
    if pdf_file_name.endswith('.pdf'):
        pdf_file_path = os.path.join(pdf_directory, pdf_file_name)

        full_text = open_pdf_file(pdf_file_path)
        pdf_tax_dict = extract_tax_info_from_pdf(full_text)
        update_row(df, pdf_tax_dict, excel_tax_codes, pdf_file_path)
        time.sleep(taio_constant.RETRY_MAX)

