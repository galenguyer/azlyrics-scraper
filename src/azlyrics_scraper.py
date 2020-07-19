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
    if not url.startswith('https://www.azlyrics.com/lyrics/'):
        eprint(f'URL "{url}" does not appear to be a valid azlyrics url')
        return None
    result = requests.get(url)
    if result.status_code != 200:
        eprint(f'Status code {result.status_code} for url "{url}" indicates failure')
        return None
    parsed_page = BeautifulSoup(result.text, 'html.parser')
    # lyrics are consistently on the 20th div in the page
    lyrics = parsed_page.find_all('div', limit=21)[-1].get_text().strip()
    artist = parsed_page.find_all('b')[0].get_text().strip().rsplit(' ', 1)[0]
    song_title = parsed_page.find_all('b')[1].get_text().strip('" ')


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
