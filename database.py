import requests
import sqlite3
import re 
api_key_tmdb = "47b3a635b1af2202b8148087b4c27d5c"
api_key_omdb = 'c7d0425c'

def database_setup(cur):
    """Function used to create databases"""
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        original_title TEXT,
        genre TEXT,
        runtime INTEGER,
        year INTEGER
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Preformance (
        movie_id INTEGER PRIMARY KEY,
        rating INTEGER,
        box_office INTEGER,
        nominations INTEGER,
        awards INTEGER,
        FOREIGN KEY (movie_id) REFERENCES Movies(id)
    )
    ''')


def fetch_titles_from_years(year):
    """Fetch movie tittles for movies released between start_year and end_year"""
    all_movies = []

    url = f"https://api.themoviedb.org/3/discover/movie?primary_release_year={year}&api_key={api_key_tmdb}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("results", [])
        for movie in results:
            all_movies.append({"title": movie.get("title"),"original_title": movie.get("original_title")})
    else:
        print(f"Failed to fetch data for year {year}: {response.status_code}")
    
    return all_movies


def fetch_movie_information(movies):
    """Fetches descriptive information about the movie"""
    for movie in movies:
        title = movie['title']
        url = f"http://www.omdbapi.com/?t={title}&apikey={api_key_omdb}"
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            movie['genre'] = results.get("Genre")
            movie['runtime'] = results.get("Runtime")
            movie['year'] = results.get("Year")
        else:
            print(f"Failed to fetch information for movie {title}: {response.status_code}")
    
    return movies


def fetch_preformance_information(movies):
    """Fetches descriptive information about the movie"""
    for movie in movies:
        title = movie['title']
        url = f"http://www.omdbapi.com/?t={title}&apikey={api_key_omdb}"
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            movie['rating'] = results.get("Ratings")
            movie['imdbRating'] = results.get("imdbRating")
            movie['awards'] = results.get("Awards")
            movie['boxoffice'] = results.get("BoxOffice")
        else:
            print(f"Failed to fetch information for movie {title}: {response.status_code}")
    
    return movies


def parse_rating(value):
    if '/' in value:
        num, denom = value.split('/')
        return float(num) / float(denom) * 10 if float(denom) != 10 else float(num)
    elif '%' in value:
        return float(value.strip('%')) / 10
    else:
        return None


def parse_awards(awards_str):
    if not awards_str or awards_str == 'N/A':
        return -1, -1
    wins = sum(map(int, re.findall(r'(\d+)\s+win', awards_str)))
    noms = sum(map(int, re.findall(r'(\d+)\s+nomination', awards_str)))
    return wins, noms


def parse_box_office(value):
    if not value or value == "N/A":
        return -1
    value = re.sub(r'[^\d]', '', value) 
    try:
        return int(value)
    except ValueError:
        return -1


def process_preformance(movies):
    for movie in movies:
        ratings = movie.get('rating', [])
        if not isinstance(ratings, list):
            ratings = []
        rating_values = []

        for rating in ratings:
            score = parse_rating(rating.get('Value', ''))
            if score is not None:
                rating_values.append(score)

       
        imdb = movie.get('imdbRating')
        if imdb and imdb != 'N/A':
            try:
                rating_values.append(float(imdb)) 
            except ValueError:
                pass

        avg_rating = round(sum(rating_values) / len(rating_values), 1) if rating_values else -1
        movie['average_rating'] = avg_rating

        awards_str = movie.get('awards', '')
        wins, noms = parse_awards(awards_str)
        movie['wins'] = wins
        movie['nominations'] = noms

        box_office_str = movie.get('boxoffice')
        movie['box_office'] = parse_box_office(box_office_str)

    return movies


def insert_movie_information(movies,cur):
    for movie in movies:
        year = int(movie['year']) if  movie['year'] not in (None, '', 'N/A') else -1
        runtime = int(movie['runtime'].split()[0]) if movie['runtime'] not in (None, '', 'N/A') else -1
        cur.execute('''
                INSERT INTO Movies (title, original_title, genre, runtime, year)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                movie['title'],
                movie['original_title'],
                movie['genre'],
                runtime,
                year
        ))


def insert_preformance_information(movies,cur):
    for movie in movies:
        cur.execute("SELECT id FROM Movies WHERE title = ?", (movie['title'],))
        result = cur.fetchone()
        movie_id = result[0]
        cur.execute('''
                INSERT INTO Preformance (movie_id, rating, box_office, nominations, awards)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                movie_id,
                movie['average_rating'],
                movie['box_office'],
                movie['nominations'],
                movie['wins']
        ))


def driver():
    """Main Application Driver"""
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Movies")
    cur.execute("DROP TABLE IF EXISTS Preformance")
    database_setup(cur)
    for year in range(2015,2025):
        movie_titles = fetch_titles_from_years(year)
        movies = fetch_movie_information(movie_titles)
        insert_movie_information(movies,cur)
        preformance = fetch_preformance_information(movie_titles)
        preformance = process_preformance(preformance)
        insert_preformance_information(preformance,cur)
    conn.commit()
    conn.close()
