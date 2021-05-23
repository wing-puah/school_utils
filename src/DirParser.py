#!/usr/bin/env python3

"""
See https://stackoverflow.com/questions/34837707/how-to-extract-text-from-a-pdf-file
"""
import os
import glob

import fitz
from PyPDF2 import PdfFileReader

thisdir = os.getcwd()


class DirParser:
    def __init__(self, dir_name="/files_to_parse"):
        self.file_dir = dir_name

    def parse(self):
        dir_path = f'{thisdir}{self.file_dir}'
        pdf_files_path = glob.glob(f'{dir_path}/*.pdf')

        if len(pdf_files_path) == 0:
            raise Exception('There is no files to be parsed')

        for filename in pdf_files_path:
            doc = fitz.open(filename)
            pages = doc.page_count
            print(pages)
            page1 = doc.load_page(21)
            print(page1.getText('words'))
            # content = textract.process(filename)
            # print(content)
            # pdf_reader = PdfFileReader(open(filename, 'rb'))
            # pages = pdf_reader.numPages
            # print('page: ', pdf_reader.getPage(2).extractText())
            # for i in range(pages):
            #     page_text = pdf_reader.getPage(i).extractText()
            # print(page_text)
            # print(pages)
            # print(filename)
            # pdf_reader = PdfFileReader(open(filename), 'rb')
            # print(pdf_reader)
