#!/usr/bin/env python3
import os
import glob

thisdir = os.getcwd()


class DirParser:
    def __init__(self, dir_name="/files_to_parse"):
        self.file_dir = dir_name

    def parse(self):
        print(thisdir, 'file dir', self.file_dir)
        dir_path = f'{thisdir}{self.file_dir}'
        # os.path.join(thisdir, self.file_dir)
        print(dir_path)
        print(glob.glob(f'{dir_path}/*.pdf'))
