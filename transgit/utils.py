from colorama import Fore, Back


def colored(text, *colors):
    return ''.join(colors) + text + Fore.RESET + Back.RESET
