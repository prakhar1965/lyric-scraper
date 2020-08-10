import urllib.request
from bs4 import BeautifulSoup

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
    title = input("Enter Song Title :)")
    artist = input("Enter Song Artist :)")
    print("Finding lyrics for " + title + "...............")
    lyric = find_lyrics(title, artist)
    if not lyric:
        print("Sorry, lyric for this song couldn't be found :(")
    else:
        print('\n' + title.upper() + " - " + artist.upper() + " LYRICS\n" + lyric)
