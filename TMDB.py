import tmdbsimple as tmdb
import requests
import yaml

tmdb.API_KEY = '79e53e7fdbfb5dc5fe76b8085734401c'

movie = "armageddon"


def fix_title(movie_title, signal):
    """Remove unrelated characters from title"""
    sign_to_space = ['.', '(', '[', '{']
    sign_to_empty = [')', ']', '}', '́', 'hd', '720p', '1080p', '720', '1080', 'blu-ray', 'dvd', 'remux']

    movie_title = movie_title.lower()

    for sign in sign_to_space:
        if sign in movie_title:
            movie_title = movie_title.replace(sign, ' ')

    for sign in sign_to_empty:
        if sign in movie_title:
            movie_title = movie_title.replace(sign, '')

    if '&' in movie_title:
        movie_title = movie_title.replace('&', 'and')

    year_from_title = [int(s) for s in movie_title.split() if s.isdigit()]
    for i in year_from_title:
        if len(str(i)) == 4:
            year_from_title = str(i)
            movie_title = movie_title[0:movie_title.find(year_from_title)]  # Remove year and all the text after from movie_title

    if isinstance(year_from_title, list):
        year_from_title = ''

    print(movie_title)
    signal.emit(movie_title)

    return search_tmdb(movie_title, year_from_title)


def search_tmdb(movie_title, year_from_title):
    """Search TMDB, get ID and then filter results"""
    search = tmdb.Search()
    response = search.movie(query=movie_title)
    if search.results == []:
        print(movie_title + ' returned no results')
        return

    # for s in search.results:
    #     print(s['title'], s['id'], s['release_date'], s['popularity'])


    other_movies_id = []
    result_id = ''

    for s in search.results:
        if (s['title'].lower()) == movie_title:  # checks if names are matched
            result_id = s['id']
            break

    if result_id == '':
        for s in search.results:
            if year_from_title in s['release_date']:  # if there's year, match it to results
                result_id = s['id']
                break

    try:
        return get_tmdb_url_data(result_id)
        # return get_movie_info(result_id)
    except Exception as err:
        print("Can't find '" + movie_title + "' on TMDB.com")

    if result_id == '':
        for s in search.results:
            other_movies_id.append(s['id'])  # if none of the above, pass the first result
        return get_tmdb_url_data(other_movies_id[0])
        # return get_movie_info(other_movies_id[0])


def get_tmdb_url_data(movie_id):
    link = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + '?api_key=' + tmdb.API_KEY + '&language=hebrew'
    image_url = "http://image.tmdb.org/t/p/w640/"
    # print (link)
    f = requests.get(link)

    result = f.text
    result = result.replace('false', 'False')
    result = result.replace('true', 'True')
    result = yaml.load(result)

    id = str(result['id'])
    tmdb_title = result['original_title']
    poster_front = image_url + result['poster_path']
    release_date = result['release_date']
    vote = result['vote_average']

    try:
        poster_back = ''
        poster_back = image_url + result['backdrop_path']
    except: IndexError

    try:
        genre_1 = ''
        genre_1 = result['genres'][0]['name']
    except: IndexError

    try:
        genre_2 = ''
        genre_2 = result['genres'][1]['name']
    except: IndexError

    try:
        genre_3 = ''
        genre_3 = result['genres'][2]['name']
    except: IndexError

    try:
        overview = ''
        overview = result['overview']
    except: IndexError

    try:
        runtime = ''
        runtime = result['runtime']
    except: IndexError

    adict = {'tmdb_title': tmdb_title,
            'release_date': release_date,
            'vote': vote,
            'poster_front': poster_front,
            'runtime': runtime,
            'id': id,
            'genre_1': genre_1,
            'genre_2': genre_2,
            'genre_3': genre_3,
            'poster_back': poster_back,
            'overview':overview
            }

    return adict

# def get_movie_info(id):
#     """Get all relevant info from TMDB"""
#     image_url = "http://image.tmdb.org/t/p/w640/"
#     identity = tmdb.Movies(id)
#     response = identity.info()
#
#     title = identity.title
#     release_date = identity.release_date
#     vote = identity.vote_average
#     poster_front = image_url + identity.poster_path
#     id = identity.id
#
#     try:
#         runtime = 'None'
#         runtime = str(datetime.timedelta(minutes=identity.runtime))
#     except: IndexError
#
#     try:
#         genre_1 = 'None'
#         genre_1 = (identity.genres[0])['name']
#     except: IndexError
#
#     try:
#         genre_2 = 'None'
#         genre_2 = (identity.genres[1])['name']
#     except: IndexError
#
#     try:
#         genre_3 = 'None'
#         genre_3 = (identity.genres[2])['name']
#     except: IndexError
#
#     try:
#         poster_back = 'None'
#         poster_back = image_url + identity.backdrop_path
#     except: IndexError
#
#     try:
#         overview = 'None'
#         overview = identity.overview
#     except: IndexError
#
#     dict = {'tmdb_title': title,
#             'release_date': release_date,
#             'vote': vote,
#             'poster_front': poster_front,
#             'runtime': runtime,
#             'id': id,
#             'genre_1': genre_1,
#             'genre_2': genre_2,
#             'genre_3': genre_3,
#             'poster_back': poster_back,
#             'overview': overview
#             }
#     return dict

# fix_title(movie)

