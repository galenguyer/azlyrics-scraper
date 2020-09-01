import os 
import argparse
import json
from json import JSONEncoder
import re
import sys
import requests
from bs4 import BeautifulSoup


class Song:
    def __init__(self, title: str, artist: str, album: str, release: str, lyrics: str, url: str):
        self.title = title
        self.artist = artist
        self.album = album
        self.release = release
        self.lyrics = lyrics
        self.url = url


class SongEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class SearchResult:
    def __init__(self, result):
        self.link = result.a['href']
        self.title = result.a.b.text.strip('" ')
        self.artist = result.find_all('b')[1].text

    def __str__(self):
        return f'{self.title} by {self.artist}'


def eprint(*args, **kwargs):
    """
    Print the given message to stderr
    """
    print(*args, file=sys.stderr, **kwargs)


def search(term: str) -> str:
    """
    Search for a term
    """
    original_term = term
    term = re.sub('[^a-zA-Z0-9 ]+', '', term).strip()
    term = re.sub(' ', '+', term)
    search_page = requests.get(f'https://search.azlyrics.com/search.php?q={term}&w=songs&p=1')
    if search_page.status_code != 200:
        eprint(f'Status code {search_page.status_code} for search term "{original_term}" indicates failure')
        return None
    parsed_page = BeautifulSoup(search_page.text, 'html.parser')
    search_results = parsed_page.find_all('td', attrs={"class": "text-left visitedlyr"})
    results = [SearchResult(result) for result in search_results]
    if len(results) == 0:
        eprint(f'No songs found for query {original_term}')
        sys.exit(1)
    if len(results) is 1:
        print(f'Only result found is {results[0]}')
        return results[0].link
    for num in range(1, min(16, len(results)+1)):
        print(f'{num}. {results[num-1]}')
    result = results[int(input('Select a number: '))-1]
    return result.link


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
    lyrics = parsed_page.find_all('div', limit=21)[-1].text.strip()
    artist = parsed_page.find_all('b')[0].text.strip().rsplit(' ', 1)[0]
    song_title = parsed_page.find_all('b')[1].text.strip('" ')
    album_info = parsed_page.find_all('div', attrs={"class": "songinalbum_title"})[0]
    album = album_info.b.text.strip('" ')
    year = album_info.text.rsplit(' ', 1)[1].strip('( )')
    return Song(title=song_title, artist=artist, album=album, release=year, lyrics=lyrics, url=url)


def save_to_file(song: Song):
    filename = './lyrics/azlyrics_'
    for c in song.title.lower():
        if c.isalpha() or c.isdigit():
            filename = filename + c
        if c is ' ':
            filename = filename + '-'
    filename = filename + '_'
    for c in song.artist.lower():
        if c.isalpha() or c.isdigit():
            filename = filename + c
        if c is ' ':
            filename = filename + '-'
    filename = filename + '.json'
    if not os.path.isdir('./lyrics'):
        os.mkdir('./lyrics')
    f = open(filename, 'w')
    json.dump(song, f, indent=4, cls=SongEncoder)
    f.close()
    print('Lyrics saved to ' + filename)


def main():
    parser = argparse.ArgumentParser(description='Scraper for lyrics from azlyrics.com')
    parser.add_argument('term', metavar='TERM', help='Term to search for', nargs='+')
    parser.add_argument('--no-save', help='Whether or not to save the data to a file', action='store_false')
    args = parser.parse_args()

    if args.term is not None:
        term = ' '.join(args.term)
        if term.startswith('https://www.azlyrics.com/lyrics/'):
            song = download_url(term)
        else:
            song = download_url(search(term))
        if args.no_save:
            save_to_file(song)
        else:
            print('Title: ' + song.title)
            print('Artist: ' + song.artist)
            print('Album: ' + song.album + '\n')
            print(song.lyrics)
    else:
        eprint('No URL given, doing nothing')


if __name__ == '__main__':
    main()
