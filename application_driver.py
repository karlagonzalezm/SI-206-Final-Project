import requests
import sqlite3
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
        awards TEXT,
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


def insert_movie_information(movies,cur):
    for movie in movies:
        cur.execute('''
                INSERT INTO Movies (title, original_title, genre, runtime, year)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                movie['title'],
                movie['original_title'],
                movie['genre'],
                movie['runtime'],
                movie['year']
        ))


def main():
    """Main Application Driver"""
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Movies")
    cur.execute("DROP TABLE IF EXISTS Preformance")
    database_setup(cur)
    for year in range(2020,2025):
        movie_titles = fetch_titles_from_years(year)
        movies = fetch_movie_information(movie_titles)
        insert_movie_information(movies,cur)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()