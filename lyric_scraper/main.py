import os
import click
import eyed3
import urllib.request
from bs4 import BeautifulSoup

@click.command()
@click.option('-s', is_flag=True, help='If [FILES] is provided, Lyrics will be saved in file metadata')
@click.option('-t', is_flag=True, help='This option makes a new .txt file and save lyric in this file')
@click.option('-a', is_flag=True, help="if [FILES] is provided, if lyric of file can't be found from metadata that file will be skipped")
@click.argument('files', nargs=-1, type=click.File('rb', 'wb'))
def to_get_lyrics(files, a, s, t):
    """Welcome to lyric_scraper :)
       I'm Prakhar Omar from NIT Trichy.

       Use following command:

       1. lyrics: it will prompt to enter song details, Lyrics wll be printed on standard output.

       2. lyrics [FILES] : it will take files as argument, and will get lyrics from metadata.

       THANKS. Happy Coding :)

       Source Code at https://github.com/prakhar1965/lyric-scraper.

       Read the following options for more details:

    """
    #To show only warnings.
    eyed3.log.setLevel("ERROR")
    if files:
        for file in files:
            # print(os.path.dirname(os.path.realpath(__file__)))
            # Only support for .mp3 file
            if not file.name.endswith(".mp3"):
                click.secho(file.name + " file is not supported", fg='red')
                continue
            try:
                # To load meta data from .mp3 file
                song_meta = eyed3.load(file.name)
            except ValueError:
                click.secho(file.name + " format is not supported", fg='red')
                return
            try:
                title = song_meta.tag.title
                artist = song_meta.tag.artist
                lyric = find_lyrics(title, artist)
                if not lyric:
                    if a:
                        click.secho(file.name + " skipped", fg='red')
                        continue
                    click.secho("Lyric can't be found with metadata, Please enter details for "+file.name, fg='red')
                    title = input("Enter Song Title for :) ")
                    artist = input("Enter Song Artist :) ")
                    lyric = find_lyrics(title, artist)
                    song_meta.tag.title = title
                    song_meta.tag.artist = artist
                    song_meta.tag.save()
            except AttributeError:
                # Condition for skip the file
                if a:
                    click.secho(file.name + " skipped", fg='red')
                    continue
                click.secho("Song metadata is missing, Please enter details for "+file.name, fg='red')
                title = input("Enter Song Title :) ")
                artist = input("Enter Song Artist :) ")
                lyric = find_lyrics(title, artist)
                song_meta.tag.title = title
                song_meta.tag.artist = artist
                song_meta.tag.save()
            if s:
                if not lyric:
                    click.secho("Lyrics can't be found for "+file.name, fg='red')
                song_meta.tag.lyrics.set(lyric)
                try:
                    song_meta.tag.save()
                    click.secho("Lyrics Successfully saved for "+file.name, fg='green')
                except NotImplementedError:
                    click.secho("Error in saving lyrics for "+file.name, fg='red')
            if t:
                #To save lyrics in txt format
                dir_file = os.path.dirname(os.path.realpath(__file__))
                text_file = open(dir_file+"/"+song_meta.tag.title.replace(' ', '-')+".txt", "w")
                text_file.write('\n'+song_meta.tag.title.upper()+" - "+song_meta.tag.artist.upper()+" LYRICS\n"+lyric)
                click.secho("Lyrics are saved in  "+dir_file+"/"+song_meta.tag.title.replace(' ', '-')+".txt for "+file.name, fg='green')
                text_file.close()
            if not s and not t:
                if not lyric:
                    click.secho("Lyrics can't be found for "+file.name, fg='red')
                else:
                    click.secho('\n'+song_meta.tag.title.upper()+" - "+song_meta.tag.artist.upper()+" LYRICS\n"+lyric, fg='blue')
    elif not files and s:
        click.secho("Please provide file to save in metadata", fg='red')

    else:
        title = input("Enter Song Title :) ")
        artist = input("Enter Song Artist :) ")
        click.secho("Finding lyrics for " + title + "...............", fg='yellow')
        lyric = find_lyrics(title, artist)
        if not lyric:
            click.secho("Sorry, lyric for this song couldn't be found :(", fg='red')
        else:
            if t:
                dir_file = os.getcwd()
                text_file = open(dir_file + "/" + title.replace(' ', '-') + ".txt", "w")
                text_file.write('\n' + title.upper() + " - " + artist.upper() + " LYRICS\n" + lyric)
                click.secho("Lyrics are saved in  " + dir_file + "/" + title.replace(' ', '-') + ".txt", fg='green')
                text_file.close()
            else:
                click.secho('\n' + title.upper() + " - " + artist.upper() + " LYRICS\n" + lyric, fg='blue')


def find_lyrics(song_title, song_artist):
    search_query = song_title.lower() + ' ' + song_artist.lower()
    # String for performing search query
    search_query = "-".join(search_query.split(' '))
    url = 'https://search.azlyrics.com/search.php?q=' + search_query
    # To perform search query on AZlyrics.com
    content = urllib.request.urlopen(url)
    html_text = content.read()
    soup = BeautifulSoup(html_text, 'html.parser')
    lyric_found = False
    # To find all the tags which contain lyric link
    for tag in soup.find_all('td', {'class': 'text-left visitedlyr'}):
        if tag.a:
            lyric_found = True
            lyric_url = tag.a['href']
            break
    if not lyric_found:
        # print("lyric couldn't be found for given title")
        return
    lyric_content = urllib.request.urlopen(lyric_url)
    lyric_html = lyric_content.read()
    lyric_soup = BeautifulSoup(lyric_html, 'html.parser')
    for div in lyric_soup.find_all('div', {'class': 'col-xs-12 col-lg-8 text-center'}):
        inner_div = div
        for div in inner_div.find_all('div'):
            if not div.has_attr('class'):
                return div.text
    return


if __name__ == '__main__':
    to_get_lyrics()

