import requests
import yaml
key = '79e53e7fdbfb5dc5fe76b8085734401c'


def get_tmdb_data(movie_id):
    image_url = "http://image.tmdb.org/t/p/w640/"
    link = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + '?api_key=' + key + '&language=hebrew'
    f = requests.get(link)

    result = f.text
    result = result.replace('false', 'False')
    result = result.replace('true', 'True')
    result = yaml.load(result)

    try:
        poster_back, genre_1, genre_2, genre_3, runtime, overview = '', '', '', '', '', ''

        id = str(result['id'])
        name = result['original_title']
        poster_path = image_url + result['poster_path']
        backdrop_path = image_url + result['backdrop_path']
        genre1 = result['genres'][0]['name']
        genre2 = result['genres'][1]['name']
        genre3 = result['genres'][2]['name']
        overview = result['overview']
        release_date = result['release_date']
        runtime = result['runtime']
        vote_average = result['vote_average']
        tmdb_link = 'https://www.themoviedb.org/movie/' + id
    except: IndexError

    print(poster_path)


get_tmdb_data(10749)
