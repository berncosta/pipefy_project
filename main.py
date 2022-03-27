# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pipefy_handler import pipefy_handler


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    pipefy_token = ""
    new_pipe = pipefy_handler.pipefyHandler(pipefy_token, 301510364)
    cards = new_pipe.get_all_cards_as_pandas()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
