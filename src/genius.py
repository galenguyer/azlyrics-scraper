import argparse
import sys
import requests
from bs4 import BeautifulSoup


def eprint(*args, **kwargs):
    """
    Print the given message to stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def download_url(url: str):
    """
    Retrieve the page contents and parse out the lyrics from a given url
    """
    if not url.startswith('https://genius.com/'):
        eprint(f'URL "{url}" does not appear to be a valid genius lyrics url')
        return None
    result = requests.get(url)
    if result.status_code != 200:
        eprint(f'Status code {result.status_code} for url "{url}" indicates failure')
        return None
    parsed_page = BeautifulSoup(result.text, 'html.parser')
    lyrics = parsed_page.find_all('div', attrs={'class': 'lyrics'})[0].text.strip()
    print(lyrics)


def main():
    parser = argparse.ArgumentParser(description='Scraper for lyrics from genius.com')
    parser.add_argument('-u', '--url', help='Direct URL of a song to download')
    args = parser.parse_args()

    if args.url is not None:
        download_url(args.url)
    else:
        eprint('No URL given, doing nothing')


if __name__ == '__main__':
    main()
