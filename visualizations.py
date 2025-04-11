import matplotlib.pyplot as plt

movie_data = {'Adventure': {'count': 84, 'avg_rating': 7.04, 'avg_box_revenue': 257460015.85, 'avg_award_nom_ratio': 0.43}, 'Animation': {'count': 32, 'avg_rating': 7.69, 'avg_box_revenue': 194431920.27, 'avg_award_nom_ratio': 0.62}, 'Comedy': {'count': 50, 'avg_rating': 6.68, 'avg_box_revenue': 216882544.21, 'avg_award_nom_ratio': 0.41}, 'Crime': {'count': 21, 'avg_rating': 6.77, 'avg_box_revenue': 128161137.67, 'avg_award_nom_ratio': 0.37}, 'Drama': {'count': 65, 'avg_rating': 6.67, 'avg_box_revenue': 129006901.92, 'avg_award_nom_ratio': 0.49}, 'Fantasy': {'count': 21, 'avg_rating': 6.48, 'avg_box_revenue': 261074561.94, 'avg_award_nom_ratio': 0.39}, 'Horror': {'count': 22, 'avg_rating': 6.38, 'avg_box_revenue': 90091731.0, 'avg_award_nom_ratio': 0.4}, 'Mystery': {'count': 15, 'avg_rating': 6.38, 'avg_box_revenue': 80208150.38, 'avg_award_nom_ratio': 0.37}, 'Romance': {'count': 21, 'avg_rating': 5.07, 'avg_box_revenue': 37144874.3, 'avg_award_nom_ratio': 0.37}, 'Sci-Fi': {'count': 33, 'avg_rating': 6.71, 'avg_box_revenue': 270744329.13, 'avg_award_nom_ratio': 0.34}, 'Thriller': {'count': 37, 'avg_rating': 6.43, 'avg_box_revenue': 118720067.48, 'avg_award_nom_ratio': 0.43}}

genres = list(movie_data.keys())

avg_ratings = [movie_data[genre]['avg_rating'] for genre in genres]
plt.figure()
plt.bar(genres, avg_ratings)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Genres')
plt.ylabel('Average Movie Rating')
plt.title('Average Movie Rating by Genre')
plt.show()


avg_box_office = [movie_data[genre]['avg_box_revenue'] / 1000000 for genre in genres]
plt.figure()
plt.bar(genres, avg_box_office)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Genres')
plt.ylabel('Average Box Office Revenue (Millions $)')
plt.title('Average Box Office Revenue by Genre')
plt.show()


avg_award_nom = [movie_data[genre]['avg_award_nom_ratio'] for genre in genres]
plt.figure()
plt.bar(genres, avg_award_nom)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Genres')
plt.ylabel('Average Award Nomination Ratio')
plt.title('Average Award Nomination Ratio by Genre')
plt.show()






