import argparse
import json
import sys
import requests
from json import JSONEncoder
from bs4 import BeautifulSoup


class Song:
    def __init__(self, title: str, artist: str, album: str, lyrics: str, url: str):
        self.title = title
        self.artist = artist
        self.album = album
        #self.year = year
        self.lyrics = lyrics
        self.url = url


class SongEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


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
    song_lyrics = parsed_page.find_all('div', attrs={'class': 'lyrics'})[0].text.strip()
    song_artist = parsed_page.find_all('a', attrs={'class': 'header_with_cover_art-primary_info-primary_artist'})[0].text.strip()
    song_title = parsed_page.find_all('h1', attrs={'class': 'header_with_cover_art-primary_info-title'})[0].text.strip()
    song_album = parsed_page.find_all('a', attrs={'class': 'song_album-info-title'})[0].text.strip()
    song = Song(title=song_title, artist=song_artist, album=song_album, lyrics=song_lyrics, url=url)
    print(json.dumps(song, indent=4, cls=SongEncoder))


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
