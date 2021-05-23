from src.DirParser import DirParser

instructions = """
What will you like to do? Please input the number 
1. Parse the pdf in the folder. 
2. Look for corresponding text in text_to_read.csv
"""


def run_parser():
    try:
        print('initiliase parsing ...')
        DirParser().parse()
    except Exception as e:
        print(f'Issue encounter with parser: {e}')


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

    except Exception as e:
        print(f'Error encounter: {e}, please check your input')


while True:
    main()
