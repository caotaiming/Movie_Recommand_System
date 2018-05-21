from flask import Blueprint

main = Blueprint('main', __name__)

import json
from engine import RecommendationEngine

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Flask, request


@main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    logger.debug("User %s TOP ratings requested", user_id)
    top_ratings = recommendation_engine.get_top_ratings(user_id, count)
    result = '<h1>Top ' + str(count) + ' Movies for User ' + str(user_id) + '</h1>' + '<table border="1">'
    result += '<tr><td>'+ 'Movie Name' + '</td><td>'+'Expected Rating'+'</td><td>'+'Popular'+'</td></tr>'
    for x in top_ratings:
        result += '<tr><td>'+ str(x[0]) + '</td><td>'+str(x[1])+'</td><td>'+str(x[2])+'</td></tr>'
    result += '</table>'
    return result


@main.route("/<int:user_id>/ratings/<int:movie_id>", methods=["GET"])
def movie_ratings(user_id, movie_id):
    logger.debug("User %s rating requested for movie %s", user_id, movie_id)
    ratings = recommendation_engine.get_ratings_for_movie_ids(user_id, [movie_id])

    result = '<h1>Movie  ' + str(movie_id) + ' predicted rating for User ' + str(user_id) + '</h1>' + '<table border="1">'
    result += '<tr><td>'+ 'Movie Name' + '</td><td>'+'Expected Rating'+'</td><td>'+'Popular'+'</td></tr>'
    for x in ratings:
        result += '<tr><td>'+ str(x[0]) + '</td><td>'+str(x[1])+'</td><td>'+str(x[2])+'</td></tr>'
    result += '</table>'
    return result

@main.route("/ratings/top/<int:count>", methods=["GET"])
def top_counts(count):
    logger.debug("Users most popular movies")
    top_counts = recommendation_engine.get_most_rated(count)
    result = '<h1>' + str(count) + ' most popular movies </h1>' + '<table border="1">'
    result += '<tr><td>' + 'Movie Name' + '</td><td>' + 'Total Rating Received </td></tr>'
    for x in top_counts:
        result += '<tr><td>' + str(x[0]) + '</td><td>' + str(x[1]) + '</td></tr>'
    result += '</table>'
    return result

@main.route("/ratings/top_ave/<int:count>", methods=["GET"])
def top_average(count):
    logger.debug("Users highest rated movies")
    top_ave = recommendation_engine.get_highest_rating(count)
    result = '<h1>' + str(count) + ' highest rated movies (more than 25 ratings) </h1>' + '<table border="1">'
    result += '<tr><td>' + 'Movie Name' + '</td><td>' + 'Rating </td></tr>'
    for x in top_ave:
        result += '<tr><td>' + str(x[1][0]) + '</td><td>' + str(x[1][1][1]) + '</td></tr>'
    result += '</table>'
    return result

@main.route("/<int:user_id>/ratings", methods=["POST"])
def add_ratings(user_id):
    # get the ratings from the Flask POST request object
    ratings_list = list(request.form.keys())[0].strip().split("\n")
    # ratings_list = request.form.keys()[0].strip().split("\n")
    ratings_list = map(lambda x: x.split(","), ratings_list)
    # create a list with the format required by the negine (user_id, movie_id, rating)
    ratings = map(lambda x: (user_id, int(x[0]), float(x[1])), ratings_list)
    # add them to the model using then engine API
    recommendation_engine.add_ratings(ratings)

    return str(ratings)



def create_app(spark_context, dataset_path):
    global recommendation_engine

    recommendation_engine = RecommendationEngine(spark_context, dataset_path)

    app = Flask(__name__)
    app.register_blueprint(main)
    return app