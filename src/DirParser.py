#!/usr/bin/env python3

"""
See https://stackoverflow.com/questions/34837707/how-to-extract-text-from-a-pdf-file
"""
import os
import glob
import fitz
from csv import reader
from PyPDF2 import PdfFileReader

thisdir = os.getcwd()


class DirParser:
    def __init__(self, dir_name="/files_to_parse", file_to_write="pdf_extraction.csv"):
        self.file_dir = dir_name
        self.file_to_write = file_to_write
        self.init_file()

    def init_file(self):
        print("Initialising file")
        self.extracted_file = open(self.file_to_write, 'a')

        file_size = os.path.getsize(self.file_to_write)

        if file_size == 0:
            print('Empty file detected: writing header')
            self.extracted_file.write('Filename,Page no,Content\n')

    def parse(self):
        dir_path = f'{thisdir}{self.file_dir}'
        pdf_files_path = glob.glob(f'{dir_path}/*.pdf')

        if len(pdf_files_path) == 0:
            raise Exception('There is no files to be parsed')

        for filename in pdf_files_path:
            self.handle_single_file(filename)

    def handle_single_file(self, filename):
        doc = fitz.open(filename)
        no_of_pages = doc.page_count

        printed_filename = filename.replace(f'{thisdir}{self.file_dir}', '')
        print(
            f'\nWorking on: {printed_filename}, there is a total of {no_of_pages} pages')

        for page in range(no_of_pages):
            human_readable_page_no = page + 1
            page_document = doc.load_page(page)
            content = page_document.getText('text')
            self.extracted_file.write(
                f'{printed_filename},{human_readable_page_no},{content}\n')

        # this is to introduce new line after every file
        self.extracted_file.write('\n')
        print(
            f'\t...Finish with file {printed_filename}, a total of {no_of_pages} pages are parsed')
