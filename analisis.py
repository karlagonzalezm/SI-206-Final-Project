import requests
import sqlite3
import re 

def get_genres(cur):
    '''Returns a list containing all of the unique gennre ids in the database'''
    query = '''SELECT genre_id FROM Genres'''
    result = cur.execute(query).fetchall()
    return [row[0] for row in result]


def get_genre_count(genres,cur):
    '''Returns a dictioanry that contains the amount of movies belonging to each genre'''
    genre_count = {}
    for genre in genres:
        query = '''
        SELECT COUNT(id)
        FROM Movies
        WHERE ',' || genre || ',' LIKE ?
        '''
        like_pattern = f'%,{genre},%'
        count = cur.execute(query, (like_pattern,)).fetchone()[0]
        query = '''SELECT genre FROM Genres WHERE genre_id == ?'''
        genre_string =  cur.execute(query, (genre,)).fetchone()[0]
        genre_count[genre_string] = count
    return genre_count


def get_significant_genres(genre_count,cur):
    '''Returns a list only containign the significant genres'''
    genres = []
    for key,value in genre_count.items():
        if value > 10:
            query = '''SELECT genre_id FROM Genres WHERE genre == ?'''
            genre_int =  cur.execute(query, (key,)).fetchone()[0]
            genres.append(genre_int)
    return genres


def get_average_rating(genres,cur):
    '''Returns a dictioanry that matches each genre to the average rating'''
    genre_average = {}
    for genre in genres:
        query = '''
        SELECT AVG(p.rating)
        FROM Movies m 
        JOIN PREFORMANCE p ON m.id = p.movie_id
        WHERE ',' || m.genre || ',' LIKE ? AND p.rating != -1
        '''
        avg_rating = cur.execute(query,(f'%,{genre},%',)).fetchone()[0]
        query = '''SELECT genre FROM Genres WHERE genre_id == ?'''
        genre_string =  cur.execute(query, (genre,)).fetchone()[0]
        genre_average[genre_string] = round(avg_rating, 2) if avg_rating is not None else None

    return genre_average


def get_average_boxrevenue(genres,cur):
    '''Returns a dictionary with the average box revenue per genre'''
    genre_boxrevenue = {}
    for genre in genres:
        query = '''
        SELECT AVG(p.box_office)
        FROM Movies m 
        JOIN PREFORMANCE p ON m.id = p.movie_id
        WHERE ',' || m.genre || ',' LIKE ? AND p.box_office != -1
        '''
        avg_rating = cur.execute(query,(f'%,{genre},%',)).fetchone()[0]
        query = '''SELECT genre FROM Genres WHERE genre_id == ?'''
        genre_string =  cur.execute(query, (genre,)).fetchone()[0]
        genre_boxrevenue[genre_string] = round(avg_rating, 2) if avg_rating is not None else None

    return genre_boxrevenue


def get_average_ratio(genres,cur):
    '''Returns a dictionary with the average award-nomination ratio per genre'''
    genre_ratio = {}
    for genre in genres:
        query = '''
        SELECT AVG(CAST(p.awards AS FLOAT) / NULLIF(p.nominations, 0)) AS avg_award_nom_ratio
        FROM Movies m
        JOIN Preformance p ON m.id = p.movie_id
        WHERE ',' || m.genre || ',' LIKE ?
        AND p.awards != -1
        AND p.nominations != 1;
        '''
        ratio = cur.execute(query,(f'%,{genre},%',)).fetchone()[0]
        query = '''SELECT genre FROM Genres WHERE genre_id == ?'''
        genre_string =  cur.execute(query, (genre,)).fetchone()[0]
        genre_ratio[genre_string] = round(ratio, 2) if ratio is not None else None
    
    return genre_ratio


def write_to_file(genres,genre_rating, genre_count,genre_boxrevenue,genre_ratio,cur):
    '''Writes the calculations for each genres to a file'''
    with open("genre_information.txt", "w") as f:
        f.write("Genre | Movie Count | Avg Rating | Avg Box Revenue | Avg Award/Nomination Ratio\n")
        for genre in genres:
            query = '''SELECT genre FROM Genres WHERE genre_id == ?'''
            genre_string =  cur.execute(query, (genre,)).fetchone()[0]
            rating = genre_rating.get(genre_string, "N/A")
            count = genre_count.get(genre_string, "N/A")
            boxrev = genre_boxrevenue.get(genre_string, "N/A")
            ratio = genre_ratio.get(genre_string, "N/A")
            f.write(f"{genre_string} | {count}  | {rating} | {boxrev} | {ratio}\n")


def driver_analisis():
    '''Main application driver for analisis'''
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    genres = get_genres(cur)
    genre_count = get_genre_count(genres,cur)
    genres = get_significant_genres(genre_count,cur)
    genre_rating = get_average_rating(genres,cur)
    genre_boxrevenue = get_average_boxrevenue(genres,cur)
    genre_ratio = get_average_ratio(genres,cur)
    write_to_file(genres,genre_rating,genre_count,genre_boxrevenue,genre_ratio,cur)
    conn.commit()
    conn.close()
