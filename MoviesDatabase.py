import os
import TMDB
from Metadata import mkv_metadata
import xlwt
from itertools import chain
import re
from PyQt5 import QtCore


class MovieWorker(QtCore.QThread):

    def __init__(self, paths, xls_path, signal, parent=None):
        super().__init__(parent=parent)
        self.paths = paths
        self.xls_path = xls_path
        self.signal = signal

    def run(self):
        main(self.paths, self.xls_path, self.signal)


class movie(object):
    def __init__(self, title, path, tmdb_title='None', release_date='None', vote='None', poster_front='None',
                 runtime='None', id='None', genre_1='None', genre_2='None', genre_3='None', poster_back='None',
                 overview='None', resolution='None', audio_channels='None', size='None'):
        self.title = title
        self.path = path
        self.tmdb_title = tmdb_title
        self.release_date = release_date
        self.vote = vote
        self.poster_front = poster_front
        self.runtime = runtime
        self.id = id
        self.genre_1 = genre_1
        self.genre_2 = genre_2
        self.genre_3 = genre_3
        self.poster_back = poster_back
        self.overview = overview
        self.resolution = resolution
        self.audio_channels = audio_channels
        self.size = size


def dirsize(start_dirpath):
    """Receive path and return it's size"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_dirpath):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath) / 1000000000  # Convert to GB
            total_size = float("{0:.2f}".format(total_size))  # Limit float to one decimat point
    return total_size


def main(paths, xls_path, signal):
    matches = []
    for root, dirnames, filenames in chain.from_iterable(os.walk(path) for path in paths):
        for filename in filenames:
            if filename.endswith(('.mkv', '.mp4', '.avi', '.ts')):
                matches.append(os.path.join(root, filename))
        for dirname in dirnames:
            if dirname.endswith('BDMV'):
                matches.append(os.path.join(root, filename))

    movies_list = []
    for i in matches:
        for pa in paths:
            if os.name == 'POSIX':
                slashes = [m.start() for m in re.finditer(os.sep, i)][-2]  # Location of 2nd '/' from the end of full path
            else:
                slashes = [m.start() for m in re.finditer(r"\\", i)][-2]  # Location of 2nd '/' from the end of full path



            print(slashes)
            title = i[slashes:i.rfind(os.sep)]
            if os.sep in title:  # Deal with sub folders
                title = title[title.find(os.sep)+1:]
            path = i[:slashes]

            size = dirsize(path+title)  # Get folder size

        try:
            tmdb_info = TMDB.fix_title(title, signal)

            tmdb_title = tmdb_info['tmdb_title']
            release_date = tmdb_info['release_date']
            vote = tmdb_info['vote']
            poster_front = tmdb_info['poster_front']
            runtime = tmdb_info['runtime']
            id = tmdb_info['id']
            genre_1 = tmdb_info['genre_1']
            genre_2 = tmdb_info['genre_2']
            genre_3 = tmdb_info['genre_3']
            poster_back = tmdb_info['poster_back']
            overview = tmdb_info['overview']

        except Exception as err:
            print('Video not found in TMDB')
            tmdb_title = ''
            release_date = ''
            vote = ''
            poster_front = ''
            runtime = ''
            id = ''
            genre_1 = ''
            genre_2 = ''
            genre_3 = ''
            poster_back = ''
            overview = ''

        resolution, audio_channels = 'None', 'None'  # for non-mkv files

        if i.endswith('.mkv'):
            try:
                mkv_info = mkv_metadata(i)  # Call MKV metadata function
                resolution = mkv_info['resolution']
                audio_channels = mkv_info['audio_channels']
                runtime = mkv_info['runtime']
            except: IndexError

        a = movie(title, path, tmdb_title, release_date, vote, poster_front, runtime, id, genre_1, genre_2, genre_3, poster_back, overview, resolution, audio_channels, size)
        movies_list.append(a)

    header = 'Title, Path, TMDB Title, Release Date, Vote, Poster Front, Runtime, TMDB_Link, Gentre 1, Genre 2, Genre 3, Poster Back, Overview, Resolution, Audio Channels, Size (GB)'.split(',')

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Movies")
    style_bold = xlwt.easyxf('font: bold 1')
    style_red = xlwt.easyxf('font: color red;')
    style_bold_blue = xlwt.easyxf('font: bold 1, color blue;')

    column = 0
    for col in range(0, len(header)):
        sheet.col(column).width = 256 * 15
        column += 1
    sheet.col(0).width = 256 * 60
    sheet.col(1).width = 256 * 30
    sheet.col(2).width = 256 * 60
    sheet.col(12).width = 256 * 150


    column = 0
    for head in header:
        sheet.write(0, column, head, style_bold)  # row, column, value
        column += 1

    row = 1
    for i in movies_list:
        sheet.write(row, 0, i.title)  # row, column, value
        sheet.write(row, 1, i.path)
        sheet.write(row, 2, i.tmdb_title)
        sheet.write(row, 3, i.release_date[:4])
        sheet.write(row, 4, i.vote)
        if i.poster_front == "":
            sheet.write(row, 5, i.poster_front)
        else:
            sheet.write(row, 5, xlwt.Formula('HYPERLINK("%s";"Link")' % i.poster_front), style_bold_blue)
        sheet.write(row, 6, i.runtime)
        sheet.write(row, 7, xlwt.Formula('HYPERLINK("%s";"Link")' % ('http://www.themoviedb.org/movie/' + str(i.id))), style_bold_blue)
        sheet.write(row, 8, i.genre_1)
        sheet.write(row, 9, i.genre_2)
        sheet.write(row, 10, i.genre_3)
        if i.poster_back == "":
            sheet.write(row, 11, i.poster_back)
        else:
            sheet.write(row, 11, xlwt.Formula('HYPERLINK("%s";"Link")' % i.poster_back), style_bold_blue)
        sheet.write(row, 12, i.overview)
        sheet.write(row, 13, i.resolution)
        sheet.write(row, 14, i.audio_channels)
        sheet.write(row, 15, i.size)

        row += 1

    workbook.save(xls_path + os.sep + "VideoFiles.xls")



# main(['/Users/amitpozner/Desktop/Movies', '/Users/amitpozner/Desktop/Movies_2'], '/Users/amitpozner/Desktop/Movies_2')