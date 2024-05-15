from datetime import date
from movie import Movie, Genre, Person
from pandas import Series, DataFrame
import pandas as pd
import requests
from kivy.app import App
from kivy.uix.label import Label


class RecommendationSystem():
    def __init__(self) -> None:
        self.liked_movies: DataFrame = DataFrame(
            columns=[
                'imdb_id',
                'title',
                'genre',
                'runtime',
                'release_date',
                'poster_url',
                'director',
                'writer',
                'actors',
                'liked'])
        self.liked_genres: Series[str] = Series()
        self.liked_directors: Series[str] = Series()
        self.liked_writers: Series[str] = Series()
        self.liked_actors: Series[str] = Series()

        self.loaded_movies: list[Movie] = []


    def movie_query(self, query:str) -> list[Movie]:
        if not query:
            return

        # Make API request to OMDB
        api_key = '3ade98ca'  # Replace with your OMDB API key
        url = f'http://www.omdbapi.com/?apikey={api_key}&s={query}&type=movie'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            self.loaded_movies.clear()

            
            # Display search results in MovieList
            if 'Search' in data:
                for movie in data['Search']:
                    new_movie = Movie()
                    new_movie.from_omdb_dict(movie)
                    

                    url2 = f'http://www.omdbapi.com/?apikey={api_key}&i={new_movie.imdb_id}'
                    response2 = requests.get(url2)
                    if response2.status_code == 200:
                        data2 = response2.json()
                        new_movie.from_omdb_dict(data2)

                    new_movie.liked = self.is_movie_liked(new_movie)
                    new_movie.genre = self.init_genres_liked(new_movie.genre)
                    new_movie.director = self.init_directors_liked(new_movie.director)
                    new_movie.writer = self.init_writers_liked(new_movie.writer)
                    new_movie.actors = self.init_actors_liked(new_movie.actors)

                    self.loaded_movies.append(new_movie)
        else:
            print(f"Error: {response.status_code} - {response.text}")
        
        return self.loaded_movies



    def is_movie_liked(self, movie:Movie) -> bool:
        return movie.imdb_id in self.liked_movies['imdb_id'].values

    def is_genre_liked(self, genre:Genre) -> bool:
        return genre.name in self.liked_genres.values
    
    def init_genres_liked(self, genre_list:list[Genre]) -> list[Genre]:
        for i in range(len(genre_list)):
            genre_list[i].liked = self.is_genre_liked(genre_list[i])
        return genre_list
        

    def is_director_liked(self, director:Person) -> bool:
        return director.name in self.liked_directors.values
    
    def init_directors_liked(self, director_list:list[Person]) -> list[Person]:
        for i in range(len(director_list)):
            director_list[i].liked = self.is_director_liked(director_list[i])
        return director_list
        
    
    def is_writer_liked(self, writer:Person) -> bool:
        return writer.name in self.liked_writers.values
    
    def init_writers_liked(self, writer_list:list[Person]) -> list[Person]:
        for i in range(len(writer_list)):
            writer_list[i].liked = self.is_writer_liked(writer_list[i])
        return writer_list

    def is_actor_liked(self, actor:Person) -> bool:
        return actor.name in self.liked_actors.values
    
    def init_actors_liked(self, actor_list:list[Person]) -> list[Person]:
        for i in range(len(actor_list)):
            actor_list[i].liked = self.is_actor_liked(actor_list[i])
        return actor_list


    def set_liked_movie(self, movie, liked):
        movie.liked = liked
        if liked:
            df_movie = pd.DataFrame([movie.to_dict()])
            self.liked_movies = pd.concat(
                [self.liked_movies, df_movie],
                ignore_index=True)
            self.update_liked_movies_ui(movie, add=True)
        else:
            self.liked_movies = self.liked_movies.drop(self.liked_movies[self.liked_movies['imdb_id'] == movie.imdb_id].index)
            self.update_liked_movies_ui(movie, add=False)
        print(self.liked_movies)


    def update_liked_movies_ui(self, movie, add):
        print("Attempting to update UI...")
        try:
            from movie_list_element import MovieListElement  # Local import to avoid circular dependency
            app = App.get_running_app()
            print("App instance:", app)
            root_widget = app.root
            print("Root widget:", root_widget)
            print("Root ids available:", root_widget.ids)

            if 'liked_movies_list' in root_widget.ids:
                movie_list_widget = root_widget.ids.liked_movies_list
                print("Movie list widget found:", movie_list_widget)

                if add:
                    movie_element = MovieListElement(movie, self)
                    movie_list_widget.add_widget(movie_element)
                    print(f"Added movie to liked list: {movie.title}")
                else:
                    for child in movie_list_widget.children[:]:
                        if isinstance(child, Label) and child.text == movie.title:
                            movie_list_widget.remove_widget(child)
                            print(f"Removed movie from liked list: {movie.title}")
                            break
            else:
                print("liked_movies_list id not found")

        except Exception as e:
            print(f"Error during UI update: {e}")
        

    def set_liked_genre(self, genre:Genre, liked:bool):
        genre.liked = liked
        if liked:
            self.liked_genres.add(genre.name)
        else:
            self.liked_genres = self.liked_genres.drop(self.liked_genres[self.liked_genres == genre.name].index)

    
    def set_liked_director(self, director:Person, liked:bool):
        director.liked = liked
        if liked:
            self.liked_directors.add(director.name)
        else:
            self.liked_directors = self.liked_directors.drop(self.liked_directors[self.liked_directors == director.name].index)

    def set_liked_writer(self, writer:Person, liked:bool):
        writer.liked = liked
        if liked:
            self.liked_writers.add(writer.name)
        else:
            self.liked_writers = self.liked_writers.drop(self.liked_writers[self.liked_writers == writer.name].index)

        
    def set_liked_actor(self, actor:Person, liked:bool):
        actor.liked = liked
        if liked:
            self.liked_directors.add(actor.name)
        else:
            self.liked_actors = self.liked_actors.drop(self.liked_actors[self.liked_actors == actor.name].index)


# Placeholding code for a base algorithm that suggests movies with the same director
    
    def generate_recommendations(self):
        # Assuming that liked_movies DataFrame has already been populated with liked movies
        liked_directors = self.liked_movies['director'].explode().unique()
        print(f"Liked directors: {liked_directors}")
        recommendations = []

        for director in liked_directors:
            if director:
                print(f"Fetching movies by director: {director}")
                director_recommendations = self.fetch_movies_by_director(director)
                print(f"Found {len(director_recommendations)} movies for director {director}")
                recommendations.extend(director_recommendations)

        recommendations_df = pd.DataFrame(recommendations).drop_duplicates(subset=['imdb_id'])
        print(f"Generated recommendations: {recommendations_df}")
        return recommendations_df
