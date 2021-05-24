#!/usr/bin/env python3

"""
See https://stackoverflow.com/questions/34837707/how-to-extract-text-from-a-pdf-file
"""
import os
import glob
import fitz
import json
import re

from csv import reader, writer

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
        else:
            print('Either file is missing or is not readable, creating file...')
            with open(self.file_to_write, 'w') as open_file:
                open_file.write(json.dumps({}))

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

        printed_filename = filename.replace(f'{thisdir}{self.file_dir}/', '')
        print(
            f'\nWorking on: {printed_filename}, there is a total of {no_of_pages} pages')

        text_to_add = []
        for page in range(no_of_pages):
            # human_readable_page_no = page + 1
            page_document = doc.load_page(page)
            content = page_document.getText('text').replace(
                '\xa0', ' ').replace('\n', ' ')
            # this is to escape \u\d value
            string_encode = content.encode("ascii", "ignore")
            string_decode = str(string_encode.decode())
            text_to_add.append(string_decode)

        with open(self.file_to_write, 'r') as open_file:
            file_data = json.load(open_file)

        file_data[printed_filename] = text_to_add

        with open(self.file_to_write, 'w') as open_file:
            json.dump(file_data, open_file, indent=4)
            open_file.close()

        print(
            f'\t...Finish with file {printed_filename}, a total of {no_of_pages} pages are parsed')


class FileMatcher:
    def __init__(self, file_with_keywords="keyword_to_read.csv", file_to_match_from="pdf_extraction.json"):
        self.file_with_keywords = file_with_keywords
        self.file_to_match_from = file_to_match_from

    def match(self):
        json_file = open(self.file_to_match_from, 'r')
        file_data = json.load(json_file)

        csv_file = open(self.file_with_keywords, "r+")
        csv_content = reader(csv_file)
        csv_writer = writer(csv_file)

        new_text = []
        for row in csv_content:
            if row == '':
                return
            matches = self.match_single_content(row[0], file_data)
            if matches:
                new_text.append([row[0], *matches])
            else:
                new_text.append([row[0]])

        csv_file.seek(0)
        csv_writer.writerows(new_text)

    def match_single_content(self, content_to_match, file_data):
        matches = []
        for item in file_data.items():
            key, page_value = item

            for index, single_page in enumerate(page_value):
                has_match = re.search(
                    content_to_match, single_page, flags=re.IGNORECASE)

                if has_match:
                    matches.append(f'{key}-page {index +1}')

        return matches
