from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from movie import Movie
from recommendation_system import RecommendationSystem



class MovieListElement(GridLayout):
    def __init__(self, movie:Movie, recsys:RecommendationSystem, **kwargs):
        super(MovieListElement, self).__init__(**kwargs)

        # Movie object
        self.movie = movie

        # Recommendation system
        self.recsys = recsys

        # Layout
        self.cols = 2
        self.height = 150
        self.size_hint=(1, None)

    

        # Load poster image from URL
        self.poster_img = AsyncImage(
            source=self.movie.poster_url,
            size_hint=(None, 1),
            allow_stretch=False,
            keep_ratio=True
            )
        
        # Set movie title
        movie_title_string = "[b]{0}[/b] ({1})".format(self.movie.title, self.movie.release_date.year)
        self.title_label = Label(text=movie_title_string, color="black", markup=True)
        self.title_label.font_size = 40
        self.title_label.padding = [10,0,0,0]

        # Set "liked" icon
        self.liked_img_path = 'images/heart-outline.png' if not self.movie.liked else 'images/heart-off-outline.png'
        self.liked_img = Image(
            source=self.liked_img_path,
            size_hint=(None, 1),
            width=50,
            height=50,
            allow_stretch=False,
            keep_ratio=True,
            )
        self.liked_img.bind(on_touch_down=self.on_heart_click)

        # Set tags area
        genre_list = [genre.name for genre in self.movie.genre]
        self.tag_label = Label(text="Tags: {0}".format(','.join(genre_list)), color="black")

        # Set director area
        director_list = [director.name for director in self.movie.director]
        self.director_label = Label(text="Directed by: {0}".format(','.join(director_list)), color="black")

        # Set actor area
        actor_list = [actor.name for actor in self.movie.actors]
        self.actor_label = Label(text="Featuring: {0}".format(','.join(actor_list)), color="black")

        
        # Set misc area

        self.misc_layout = GridLayout(rows=2)
        self.misc_layout.add_widget(Label(text="Duration: ", color="black"))
        self.misc_layout.add_widget(Label(text="Country: ", color="black"))


        # Layouts
        self.body_layout = GridLayout(rows=2)
        self.title_layout = GridLayout(cols=2)
        self.detail_layout = GridLayout(cols=4)


        # Title layout
        self.title_layout.add_widget(self.liked_img)
        self.title_layout.add_widget(self.title_label)

        # Detail layout
        self.detail_layout.add_widget(self.tag_label)
        self.detail_layout.add_widget(self.director_label)
        self.detail_layout.add_widget(self.actor_label)
        self.detail_layout.add_widget(self.misc_layout)

        # Body layout
        self.body_layout.add_widget(self.title_layout)
        self.body_layout.add_widget(self.detail_layout)
        

        # Add to layout
        self.add_widget(self.poster_img)
        self.add_widget(self.body_layout)
        # self.add_widget()

    # Toggle liked on heart click
    def on_heart_click(self, instance, touch):
        if self.liked_img.collide_point(*touch.pos):
            self.movie.liked = not self.movie.liked
            self.liked_img.source = 'images/heart-outline.png' if not self.movie.liked else 'images/heart-off-outline.png'
            self.recsys.set_liked_movie(self.movie, self.movie.liked)
