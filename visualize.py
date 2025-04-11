import requests
import sqlite3
import re 

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
    genre_data = read_genre_data("genre_information.txt")
    print(genre_data)