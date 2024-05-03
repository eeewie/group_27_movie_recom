from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from recommendation_system import RecommendationSystem
from gui.movie_list_element import MovieListElement

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


def user_search_query(instance):
    search_query = instance.text.strip()
    if not search_query:
        return

    movie_result_list = recsys.movie_query(search_query)
    if not movie_result_list:
        return

    movie_list = find_movie_list(App.get_running_app().root)
    if movie_list:
        movie_list.clear_widgets()
        movie_list.height = 0

    for movie_result in movie_result_list:
        new_movie_element = MovieListElement(movie_result, recsys)
        movie_list.add_widget(new_movie_element)

        # Update MovieList height dynamically
        movie_list.height += new_movie_element.height

if __name__ == '__main__':
    MovieRecomApp().run()
