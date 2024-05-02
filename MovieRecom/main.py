from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.app import App


liked_movies_list = []

class MovieListElement(GridLayout):
    def __init__(self, movie_title='Movie title', poster_path='images/image-remove-outline.png', liked=False, **kwargs):
        super(MovieListElement, self).__init__(**kwargs)

        self.cols = 3
        self.height = 150
        self.size_hint=(1, None)
        self.liked = liked
        self.movie_title = movie_title

        self.poster_img = AsyncImage(
            source=poster_path,
            size_hint=(None, 1),
            allow_stretch=False,
            keep_ratio=True
            )
        self.title_label = Label(text=movie_title, color="black")
        self.title_label.halign='left'

        self.liked_img_path = 'images/heart-outline.png' if not self.liked else 'images/heart-off-outline.png'
        
        self.liked_img = Image(
            source=self.liked_img_path,
            size_hint=(None, 1),
            width=50,
            height=50,
            allow_stretch=False,
            keep_ratio=True,
            )

        self.add_widget(self.poster_img)
        self.add_widget(self.title_label)
        self.add_widget(self.liked_img)

    def toggle_like(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.liked = not self.liked
            self.liked_img.source = 'images/heart-outline.png' if not self.liked else 'images/heart-off-outline.png'

            if self.liked:
                if self.movie_title not in liked_movies_list:
                    liked_movies_list.append(self.movie_title)
            else:
                if self.movie_title in liked_movies_list:
                    liked_movies_list.remove(self.movie_title)


class MovieList(BoxLayout):
    def __init__(self, **kwargs):
        super(MovieList, self).__init__(**kwargs)
        self.orientation='vertical'
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        

        

class SearchBar(BoxLayout):
    def __init__(self, **kwargs):
        super(SearchBar, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50
        # Create TextInput for search input
        self.search_input = TextInput(hint_text='Search...', multiline=False, size_hint=(1, 1))
        self.search_input.bind(on_text_validate=user_search_query)
        self.add_widget(self.search_input)


class MainLayout(GridLayout):
    pass

class MovieRecomApp(App):
    def build(self):

        Window.clearcolor = (1, 1, 1, 1)
        main_layout = MainLayout(rows=2)
        body_layout = GridLayout(cols=1)

        # menu_layout = StackLayout(orientation='tb-lr')

        
        # menu_layout.add_widget(Label(text="Dashboard", height=200, color="black"))
        # menu_layout.add_widget(Label(text="Search", height=200, color="black"))
        # menu_layout.add_widget(Label(text="Liked", height=200, color="black"))

        # body_layout.add_widget(menu_layout)
        # body_layout.add_widget(Label(text='Page', color="black"))

        search_bar = SearchBar()
        movie_scroll = ScrollView()
        movie_list = MovieList()
        movie_scroll.size_hint_y = 1

        movie_scroll.add_widget(movie_list)
        body_layout.add_widget(movie_scroll)
        main_layout.add_widget(search_bar)
        main_layout.add_widget(body_layout)

        return main_layout

def find_movie_list(widget):
    """Recursively find and return the MovieList widget within the widget tree."""
    if isinstance(widget, MovieList):
        return widget
    for child in widget.children:
        found = find_movie_list(child)
        if found:
            return found
    return None

import requests

def user_search_query(instance):
    search_query = instance.text.strip()
    if not search_query:
        return

    # Make API request to OMDB
    api_key = '3ade98ca'  # Replace with your OMDB API key
    url = f'http://www.omdbapi.com/?apikey={api_key}&s={search_query}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Clear existing movie list
        movie_list = find_movie_list(App.get_running_app().root)
        if movie_list:
            movie_list.clear_widgets()

        # Display search results in MovieList
        if 'Search' in data:
            for movie in data['Search']:
                movie_title = movie['Title']
                poster_path = movie['Poster']
                liked = False  # You can customize this based on user preferences
                new_movie_element = MovieListElement(movie_title=movie_title, poster_path=poster_path, liked=liked)
                movie_list.add_widget(new_movie_element)

                # Update MovieList height dynamically
                movie_list.height += new_movie_element.height
    else:
        print(f"Error: {response.status_code} - {response.text}")


if __name__ == '__main__':
    MovieRecomApp().run()
