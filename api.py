from flask import Flask, request, jsonify
import requests
import random
import numpy as np

app = Flask(__name__)

TMDB_API_KEY = "c2ddae4da825098d489b772dd70a49f8"

# Dummy Q-table for reinforcement learning
q_table = {}

# Fetch popular movies from TMDB
def fetch_popular_movies():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [movie['title'] for movie in data.get('results', [])]
    return []

# Reinforcement Learning-based recommendation

def get_recommendations(user_id):
    if user_id not in q_table:
        q_table[user_id] = {movie: random.uniform(0, 1) for movie in fetch_popular_movies()}
    
    # Select top-N movies based on Q-values
    sorted_movies = sorted(q_table[user_id].items(), key=lambda item: item[1], reverse=True)
    recommended_movies = [movie for movie, _ in sorted_movies[:5]]
    
    # Update Q-values (simple reward update for demonstration)
    for movie in recommended_movies:
        q_table[user_id][movie] += random.uniform(0.01, 0.05)
    
    return recommended_movies

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    recommendations = get_recommendations(user_id)
    return jsonify({"recommended_movies": recommendations})

if __name__ == '__main__':
    app.run(debug=True)
