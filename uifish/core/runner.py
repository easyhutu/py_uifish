from uifish.tools.suit_lib.load_suit import LoadSuits


def run_case(path=None):
    case = LoadSuits().load(path)


if __name__ == '__main__':
    run_case()
