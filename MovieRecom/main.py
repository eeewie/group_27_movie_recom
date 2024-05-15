from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from recommendation_system import RecommendationSystem
from movie_list_element import MovieListElement
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label

recsys = RecommendationSystem()


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


class MainLayout(TabbedPanel):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.do_default_tab = False  # Disable the default tab created by Kivy
        self.bind(on_current_tab=self.handle_tab_switch)
        
        # Create tabs
        search_tab = TabbedPanelItem(text='Search')
        liked_tab = TabbedPanelItem(text='Liked Movies')
        recommended_tab = TabbedPanelItem(text='Recommended')

        # Set up the search tab with a vertical BoxLayout
        search_layout = BoxLayout(orientation='vertical')
        search_bar = SearchBar()
        movie_scroll = ScrollView(size_hint_y=1)
        movie_list = MovieList()
        movie_scroll.add_widget(movie_list)

        # Add the SearchBar and the ScrollView to the search_layout
        search_layout.add_widget(search_bar)
        search_layout.add_widget(movie_scroll)

        # Add the search_layout to the search_tab
        search_tab.add_widget(search_layout)
        
        # Add tabs to the tabbed panel
        self.add_widget(search_tab)
        self.add_widget(liked_tab)
        self.add_widget(recommended_tab)
        
        # Set up liked movies tab with a vertical BoxLayout
        liked_layout = BoxLayout(orientation='vertical')
        liked_scroll = ScrollView(size_hint=(1, 1))
        self.liked_movies_list = GridLayout(cols=1, spacing=100, size_hint_y=None)
        self.liked_movies_list.bind(minimum_height=self.liked_movies_list.setter('height'))
        liked_scroll.add_widget(self.liked_movies_list)
        liked_layout.add_widget(liked_scroll)
        liked_tab.add_widget(liked_layout)
        self.ids['liked_movies_list'] = self.liked_movies_list  # Store reference to liked_movies_list
        
        
        # Set up recommended movies tab with a vertical BoxLayout
        recommended_layout = BoxLayout(orientation='vertical')
        recommended_scroll = ScrollView(size_hint=(1, 1))
        self.recommended_movies_list = GridLayout(cols=1, spacing=100, size_hint_y=None)
        self.recommended_movies_list.bind(minimum_height=self.recommended_movies_list.setter('height'))
        recommended_scroll.add_widget(self.recommended_movies_list)
        recommended_layout.add_widget(recommended_scroll)
        recommended_tab.add_widget(recommended_layout)
        self.ids['recommended_movies_list'] = self.recommended_movies_list
        
        # Explicitly set the ids dictionary
        self.ids = {
            'liked_movies_list': self.liked_movies_list,
            'recommended_movies_list': self.recommended_movies_list
        }
        print("Tabs initialized and ids set")  # Debugging statement

    def on_touch_down(self, touch):
        print("Touch event detected")  # Debugging statement
        return super(MainLayout, self).on_touch_down(touch)
    
    def handle_tab_switch(self, *args):
        print(f"Current tab: {self.current_tab.text}")  # Debugging statement
        if self.current_tab.text == 'Liked Movies':
            print("Switching to Liked Movies tab")  # Debugging statement
            self.update_liked_movies_list()
        elif self.current_tab.text == 'Recommended':
            print("Switching to Recommended tab")  # Debugging statement
            self.update_recommendations_tab()

    def update_liked_movies_list(self):
        print("Updating liked movies list...")
        self.liked_movies_list.clear_widgets()
        liked_movies = [Movie(
            imdb_id=row['imdb_id'],
            title=row['title'],
            poster_url=row['poster_url'],
            genre=row['genre'],
            director=row['director'],
            actors=row['actors'],
            release_date=row['release_date'],
            liked=row['liked']
        ) for _, row in recsys.liked_movies.iterrows()]
        for movie in liked_movies:
            movie_element = MovieListElement(movie, recsys)
            print(f"Adding movie to liked list: {movie.title}")
            self.liked_movies_list.add_widget(movie_element)
        print(f"Added liked movies to the list")

    def update_recommendations_tab(self):
        print("Updating recommendations tab...")
        self.recommended_movies_list.clear_widgets()
        recommendations = recsys.generate_recommendations()
        recommended_movies = [Movie(
            imdb_id=row['imdb_id'],
            title=row['title'],
            poster_url=row['poster_url'],
            genre=row['genre'],
            director=row['director'],
            actors=row['actors'],
            release_date=row['release_date'],
            liked=row['liked']
        ) for _, row in recommendations.iterrows()]
        for movie in recommended_movies:
            movie_element = MovieListElement(movie, recsys)
            print(f"Adding recommended movie: {movie.title}")
            self.recommended_movies_list.add_widget(movie_element)
        print(f"Added recommended movies to the list")

             
class MovieRecomApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        main_layout = MainLayout()
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
        
        print(f"Initial liked movies: {recsys.liked_movies}")

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


def user_search_query(instance):
    search_query = instance.text.strip()
    if not search_query:
        # Optionally, you could notify the user that the search query was empty.
        print("No search query provided.")
        return

    movie_result_list = recsys.movie_query(search_query)
    if not movie_result_list:
        # Notify the user that no results were found
        print("No movies found matching your search.")
        return

    movie_list = find_movie_list(App.get_running_app().root)
    if movie_list:
        movie_list.clear_widgets()
        movie_list.height = 0
    else:
        # Notify or handle the situation where the movie list UI component is not found
        print("Error: Movie list UI component not found.")
        return

    for movie_result in movie_result_list:
        new_movie_element = MovieListElement(movie_result, recsys)
        movie_list.add_widget(new_movie_element)

        # Update MovieList height dynamically
        movie_list.height += new_movie_element.height


if __name__ == '__main__':
    MovieRecomApp().run()


