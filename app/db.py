import redis
from tmdbv3api import TMDb
from tmdbv3api import Movie, Discover

redis_db = None
popular = []
now = []
top = []
movie_discovered = []
movies = []
movie=None

class DB:
    def __init__(self, host):
        self.host = host

    def connect(self):
        r = redis.Redis(host='docker_redis', port=6379, db=0)
        r.set('foo', 'bar')
        print(r.get('foo'))
        self.redis_db = r
        print("connection success")

    def getMovies(self):
        tmdb = TMDb()
        tmdb.api_key = '1dc5bcb73c0781470cb348d5e02a05a5'
        tmdb.language = 'en'
        tmdb.debug = False

        movie = Movie()
        self.movie = movie
        self.popular = movie.popular()
        self.now = movie.now_playing()
        self.top = movie.top_rated()

        discover = Discover()
        self.movie_discovered = discover.discover_movies({
            'sort_by': 'vote_average.desc'
        })

        lists = [self.top, self.now, self.popular, self.movie_discovered]
        self.all_movies = []

        for li in lists:
            for m in li:
                exist = False
                for r in self.all_movies:
                    if r.id == m.id:
                        exist = True
                if(not exist):
                    self.all_movies.append(m)

    def setKeys(self):
        for i in self.all_movies:
            self.redis_db.pipeline().hset(i.id, "vote_count" , i.vote_count)
            self.redis_db.pipeline().hset(i.id, "overview" , i.overview)
            self.redis_db.pipeline().hset(i.id, "title" , i.title)

        self.redis_db.pipeline().execute()  
        
        for i in self.all_movies:
            self.redis_db.set(i.id, i.vote_count)

        

