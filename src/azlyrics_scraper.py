import argparse
import sys


def eprint(*args, **kwargs):
    """
    print the given message to stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def download_url(url: str):
    pass


def main():
    parser = argparse.ArgumentParser(description='Scraper for lyrics from azlyrics.com')
    parser.add_argument('-u', '--url', help='Direct URL of a song to download')
    args = parser.parse_args()

    if args.url is not None:
        download_url(url=args.url)
    else:
        eprint('No URL given, doing nothing')


if __name__ == '__main__':
    main()
