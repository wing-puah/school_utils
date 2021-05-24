#!/usr/bin/env python3

"""
See https://stackoverflow.com/questions/34837707/how-to-extract-text-from-a-pdf-file
"""
import os
import glob
import fitz
import json

from csv import reader

thisdir = os.getcwd()


class DirParser:
    def __init__(self, dir_name="/files_to_parse", file_to_write="pdf_extraction.json"):
        self.file_dir = dir_name
        self.file_to_write = file_to_write
        self.init_file()

    def init_file(self):
        print("Initialising file")

        if os.path.isfile(self.file_to_write) and os.access(self.file_to_write, os.R_OK):
            print('File exists')
            self.extracted_file = open(self.file_to_write, 'r+')
        else:
            print('Either file is missing or is not readable, creating file...')
            with open(self.file_to_write, 'w') as open_file:
                open_file.write(json.dumps({}))

            self.extracted_file = open(self.file_to_write, 'r+')
            # json.dump({}, open_file)

            # self.extracted_file = open(self.file_to_write, 'r+')

        # file_size = os.path.getsize(self.file_to_write)

        # if file_size == 0:
        #     print('Empty file detected: writing header')
        #     self.extracted_file.write('Filename,Page no,Content\n')

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

        text_to_add = []
        for page in range(no_of_pages):
            # human_readable_page_no = page + 1
            page_document = doc.load_page(page)
            content = page_document.getText('text')
            text_to_add.append(content)

        file_data = json.load(self.extracted_file)
        file_data.update({[printed_filename]: text_to_add})
        # Sets file's current position at offset.
        self.extracted_file.seek(0)
        json.dump(file_data, self.extracted_file, indent=4)

        # self.extracted_file.write(
        #     f'{printed_filename},{human_readable_page_no},{content}\n')

        # this is to introduce new line after every file
        # self.extracted_file.write('\n')
        print(
            f'\t...Finish with file {printed_filename}, a total of {no_of_pages} pages are parsed')
