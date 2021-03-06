from src.FileRunner import DirParser, FileMatcher

instructions = """
What will you like to do? Please input the number 
1. Parse the pdf in the folder '.files_to_parse'. This step will out put a 'pdf_extraction.json' file, which will be used to match the coresponding keywork in 'keyword_to_read.csv'. 
2. Look for corresponding text in keyword_to_read.csv.
3. Convert python files into single page 
"""


def run_parser():
    try:
        print('Initiliase parsing ...')
        DirParser().parse()
        print('Finish parsing')
    except Exception as e:
        print(f'Issue encounter with parser: {e}')


def run_matcher():
    try:
        print('Initialise matching...')
        FileMatcher().match()
        print('Finish matching')
    except Exception as e:
        print(f'Issue encounter with matcher: {e}')


def get_user_action():
    print(instructions)
    action = input('Enter number: ')

    if not 1 <= float(action) <= 2:
        raise Exception('Invalid choice')

    return float(action)


def main():
    try:
        action = get_user_action()

        if action == 1:
            run_parser()

        if action == 2:
            run_matcher()

    except Exception as e:
        print(f'Error encounter: {e}, please check your input')


while True:
    main()
