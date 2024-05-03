import datetime
class Person():
    def __init__(self, name:str='', liked:bool=False):
        self.name = name
        self.liked = liked
    def __str__(self) -> str:
        return self.name

class Genre():
    def __init__(self, name:str='', liked:bool=False):
        self.name = name
        self.liked = liked
    def __str__(self) -> str:
        return self.name

class Movie():
    def __init__(
            self,
            imdb_id:str='',
            title:str='',
            genre:list[Genre]=[],
            runtime: int = 0, # In minutes
            release_date:datetime.date=datetime.date.today,
            poster_url:str='',
            director:list[Person]=[],
            writer:list[Person]=[],
            actors:list[Person]=[],
            liked:bool=False
            ) -> None:

        self.imdb_id = imdb_id
        self.title = title
        self.genre = genre
        self.runtime = runtime
        self.release_date = release_date
        self.poster_url = poster_url
        self.director = director
        self.writer = writer
        self.actors = actors
        self.liked = liked


    def from_omdb_dict(self, omdb_movie: dict):
        
        self.title = omdb_movie.get('Title', '')
        self.imdb_id = omdb_movie.get('imdbID', '')
        self.poster_url = omdb_movie.get('Poster', '')

        # Release Date
        
        self.release_date = datetime.date.today()
        if omdb_movie.get('Released', '') and omdb_movie['Released'] != 'N/A':
            print(omdb_movie['Released'])
            self.release_date = datetime.datetime.strptime(omdb_movie['Released'], "%d %b %Y")

        self.runtime = 0
        if omdb_movie.get('Runtime', '') and omdb_movie['Runtime'] != 'N/A':
            self.runtime = omdb_movie['Runtime'].split()[0] if omdb_movie.get('Runtime', '') else 0


        self.genre = [Genre(name=genre.strip()) for genre in omdb_movie.get('Genre', '').split(',')]
        
        self.director = [Person(name=director.strip()) for director in omdb_movie.get('Director', '').split(',')]
        self.writer = [Person(name=writer.strip()) for writer in omdb_movie.get('Writer', '').split(',')]
        self.actors = [Person(name=actor.strip()) for actor in omdb_movie.get('Actors', '').split(',')]
        
    def to_dict(self) -> dict:
        return {
            'imdb_id': self.imdb_id,
            'title': self.title,
            'genre': [g.name for g in self.genre],
            'runtime': self.runtime,
            'release_date': self.release_date.isoformat(),
            'poster_url': self.poster_url,
            'director': [d.name for d in self.director],
            'writer': [w.name for w in self.writer],
            'actors': [a.name for a in self.actors],
            'liked': self.liked
        }

