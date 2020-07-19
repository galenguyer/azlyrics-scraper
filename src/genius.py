import argparse
import sys


def eprint(*args, **kwargs):
    """
    Print the given message to stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def main():
    parser = argparse.ArgumentParser(description='Scraper for lyrics from genius.com')
    parser.add_argument('-u', '--url', help='Direct URL of a song to download')
    args = parser.parse_args()

    if args.url is not None:
        pass
    else:
        eprint('No URL given, doing nothing')


if __name__ == '__main__':
    main()
