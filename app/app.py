#FLASK
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
import os,optparse
import redis

r = redis.Redis(host='192.168.99.100', port=6379, db=0)
r.set('foo', 'bar')
print(r.get('foo'))

info = {}
from tmdbv3api import TMDb
tmdb = TMDb()
tmdb.api_key = '1dc5bcb73c0781470cb348d5e02a05a5'
tmdb.language = 'en'
tmdb.debug = False

from tmdbv3api import Movie, Discover
movie = Movie()

popular = movie.popular()
now = movie.now_playing()
top = movie.top_rated()

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
'''
print(len(movie.now_playing()))
print(len(movie.popular()))
print(len(movie.top_rated()))

discover = Discover()
movie_discovered = discover.discover_movies({
    'sort_by': 'vote_average.desc'
})

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
    detail = movie.details(idMovie)
    print(detail)
    return render_template("details.html", item = detail)

@app.route("/search")
def search():
    key = request.args.get('key', default = "Joker")
    result = movie.search(key)
    if len(result) != 0:
        result = result[0:4]
    print(result)
    return render_template("movies.html", title="Results of the search "+"'" + key +"'", list = result)

@app.route("/top")
def top_m():
    return render_template("movies.html", title="Top Rated", list=top)

@app.route("/now")
def now_m():
    return render_template("movies.html", title="Now Playing", list=now)

@app.route("/pop")
def pop():
    return render_template("movies.html", title="Popular", list=popular)

@app.route("/all")
def all():
    response = []
    lists = [top, now, popular, movie_discovered]

    for li in lists:
        for m in li:
            exist = False
            for r in response:
                if r.id == m.id:
                    exist = True
            if(not exist):
                response.append(m)
    
    print(len(response))
    return render_template("movies.html", title="All", list=response)

if __name__ == "__main__":
    debug=False
    app.run(host="0.0.0.0",debug=debug)