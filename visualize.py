import matplotlib.pyplot as plt 

def create_avg_rating(movie_data, genres):
    avg_ratings = [movie_data[genre]['avg_rating'] for genre in genres]
    ratings_bars_color = ['orange']
    plt.figure()
    plt.bar(genres, avg_ratings, color=ratings_bars_color)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Genres')
    plt.ylabel('Average Movie Rating')
    plt.title('Average Movie Rating by Genre')
    plt.tight_layout()
    plt.savefig('Average Movie Rating by Genre')
    plt.show()


def create_avg_boxrevenue(movie_data,genres):
    avg_box_office = [movie_data[genre]['avg_box_revenue'] / 1000000 for genre in genres]
    revenue_bars_color = ['blue']
    plt.figure()
    plt.bar(genres, avg_box_office, color=revenue_bars_color)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Genres')
    plt.ylabel('Average Box Office Revenue (Millions $)')
    plt.title('Average Box Office Revenue by Genre')
    plt.tight_layout()
    plt.savefig('Average Box Office Revenue by Genre')
    plt.show()


def create_avg_ratio(movie_data,genres):
    avg_award_nom = [movie_data[genre]['avg_award_nom_ratio'] for genre in genres]
    award_bars_color = ['green']
    plt.figure()
    plt.bar(genres, avg_award_nom, color=award_bars_color)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Genres')
    plt.ylabel('Average Award Nomination Ratio')
    plt.title('Average Award Nomination Ratio by Genre')
    plt.tight_layout()
    plt.savefig('Average Award Nomination Ratio by Genre')
    plt.show()


def read_genre_data(filename):
    genre_data = {}

    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines[2:]:  
        parts = [p.strip() for p in line.strip().split('|')]
        if len(parts) != 5:
            continue 

        genre = parts[0]
        try:
            count = int(parts[1])
            avg_rating = float(parts[2])
            avg_box = float(parts[3]) if parts[3] != "None" else None
            ratio = float(parts[4]) if parts[4] != "None" else None
        except ValueError:
            continue 

        genre_data[genre] = {
            "count": count,
            "avg_rating": avg_rating,
            "avg_box_revenue": avg_box,
            "avg_award_nom_ratio": ratio
        }

    return genre_data


def driver_visualize():
    '''Main application driver for visualize'''
    movie_data = read_genre_data("genre_information.txt")
    genres = list(movie_data.keys())
    create_avg_rating(movie_data,genres)
    create_avg_boxrevenue(movie_data,genres)
    create_avg_ratio(movie_data,genres)