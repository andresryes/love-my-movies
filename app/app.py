#FLASK
from flask import Flask, jsonify, render_template, request
from db import DB
app = Flask(__name__)
import os,optparse

db = DB("redis_docker")
db.connect()
db.getMovies()
db.setKeys()

print(int(db.redis_db.get('475557')))

popular = db.popular
now = db.now
top = db.top
movie_discovered = db.movie_discovered

'''
for p in now:
    print(p.id)
    print(p.title)
    print(p.overview)
    print(p.poster_path)
    print(p.popularity)
    print(p.vote_count)
    print(p.vote_average)
    print(p.release_date)

print(len(movie.now_playing()))
print(len(movie.popular()))
print(len(movie.top_rated()))
'''

'''
for i in movie_discovered:
    print(i.title)
    print(i.poster_path)
'''
# developer = os.getenv("DEVELOPER", "Me")
developer=os.getenv("DEVELOPER")

@app.route("/")
def home():
    return render_template("index.html", list=popular[0:4])

@app.route("/details")
def details():
    idMovie = request.args.get('id', default = 475557, type = int)
    detail = db.movie.details(idMovie)
    print(detail)
    return render_template("details.html", item = detail)

@app.route("/search")
def search():
    key = request.args.get('key', default = "Joker")
    result = db.movie.search(key)
    if len(result) != 0:
        result = result[0:4]
    print(result)
    return render_template("movies.html", title="Results of the search "+"'" + key +"'", list = result, db=db.redis_db)

@app.route("/top")
def top_m():
    return render_template("movies.html", title="Top Rated", list=top, db=db.redis_db)

@app.route("/now")
def now_m():
    return render_template("movies.html", title="Now Playing", list=now, db=db.redis_db)

@app.route("/pop")
def pop():
    return render_template("movies.html", title="Popular", list=popular, db=db.redis_db)

@app.route("/all")
def all():
    response = []
    response = db.all_movies
    
    print(len(response))
    return render_template("movies.html", title="All", list=response, db=db.redis_db)

@app.route("/like")
def like():
    idMovie = request.args.get('id', default = 475557, type = int)
    if db.redis_db.get(idMovie):
        print(db.redis_db.get(idMovie))
        db.redis_db.set(idMovie, int(db.redis_db.get(idMovie))+1)
        print(db.redis_db.get(idMovie))
    return "liked"


@app.route("/dislike")
def dislike():
    idMovie = request.args.get('id', default = 475557, type = int)
    if db.redis_db.get(idMovie):
        print(db.redis_db.get(idMovie))
        db.redis_db.set(idMovie, int(db.redis_db.get(idMovie))-1)
        print(db.redis_db.get(idMovie))
    return "disliked"

if __name__ == "__main__":
    debug=False
    app.run(host="0.0.0.0",debug=debug)