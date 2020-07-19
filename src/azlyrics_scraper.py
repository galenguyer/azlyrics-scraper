import sys


def eprint(*args, **kwargs):
    """
    print the given message to stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def main():
    pass


if __name__ == '__main__':
    main()
