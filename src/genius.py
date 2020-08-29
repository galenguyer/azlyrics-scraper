import os
import argparse
import json
import sys
import requests
from json import JSONEncoder
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
    parsed_page = BeautifulSoup(result.text.replace(u"\u2018", "'").replace(u"\u2019", "'"), 'html.parser')
    song_lyrics = parsed_page.find_all('div', attrs={'class': 'lyrics'})[0].text.strip()
    song_data = json.loads([line for line in result.text.split('\n') if 'TRACKING_DATA' in line][0].split('=')[1].strip(' ;'))
    song_artist = str(song_data['Primary Artist'].encode('ascii', 'ignore').decode("utf-8"))
    song_title = song_data['Title']
    song_album = song_data['Primary Album']
    song_release = song_data['Release Date']
    song = Song(title=song_title, artist=song_artist, album=song_album, lyrics=song_lyrics, url=url, release=song_release)
    return song


def save_to_file(song: Song):
    filename = './lyrics/genius_'
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
    parser = argparse.ArgumentParser(description='Scraper for lyrics from genius.com')
    parser.add_argument('-u', '--url', help='Direct URL of a song to download')
    parser.add_argument('--no-save', help='Whether or not to save the data to a file', action='store_false')
    args = parser.parse_args()

    if args.url is not None:
        song = download_url(args.url)
        if args.no_save:
            filename = './lyrics/genius_'
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
        else:
            print('Title: ' + song.title)
            print('Artist: ' + song.artist)
            print('Album: ' + song.album + '\n')
            print(song.lyrics)
    else:
        eprint('No URL given, doing nothing')



if __name__ == '__main__':
    main()
