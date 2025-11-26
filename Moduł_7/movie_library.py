import datetime
import random

class MotionPicture:
    def __init__(self, title, year, genre):
        self.title = str(title)
        self.year = str(year)
        self.genre = str(genre)
        self.views = 0

    def __str__(self):
        return f"{self.title} ({self.year})"

    def __eq__(self, other: MotionPicture):
        """Check if two MotionPicture's are the same, based on title and year."""
        return self.title == other.title and self.year == other.year
    
    def play(self):
        self.views += 1

class Movie(MotionPicture):
    def __init__(self, title, year, genre):
        super().__init__(title, year, genre)
    
    def __eq__(self, other: Movie):
        """Check if two Movies are the same, based on title and year."""
        if not isinstance(other, Movie):  # allow comparison only with Movie
            return False
        return super().__eq__(other)
        
class Series(MotionPicture):
    def __init__(self, title, year, genre, season, episode):
        super().__init__(title, year, genre)
        self.season = season
        self.episode = episode
    
    def __eq__(self, other: Series):
        """Check if two Series are the same, based on title, year, and season and episode number."""
        if not isinstance(other, Series):  # allow comparison only with Series
            return False
        return (self.title == other.title
                and self.year == other.year
                and self.season == other.season
                and self.episode == other.episode)
    
    def __str__(self):
        return f"{self.title} S{self.season:02}E{self.episode:02}"

class MovieLibrary:
    def __init__(self):
        self.collection = []
        self.registered_keys = ['title', 'year', 'genre']
    
    def _attributes_by_key(self, x, key):
        """Helper function to get the attribute(s) of an item based on the key. Returns a list of non-None attributes."""
        keys = [key] if key else self.registered_keys
        result = []
        for k in keys:
            attr = getattr(x, k, "")
            if attr is not None:
                result.append(attr)
        return result
    
    def search(self, phrase, key = "") -> list[MotionPicture]:
        """Search for motion pictures matching the given phrase in the specified key (see `registered_keys`).
        By default, searches in all registered keys."""
        if key and key not in self.registered_keys:
            raise ValueError(f"Search key '{key}' is not supported.")
        
        # Get all items where the phrase is found in the specified key(s). Case-insensitive.
        results = []
        for item in self.collection:
            attributes = self._attributes_by_key(item, key)
            if phrase.lower() in [attr.lower() for attr in attributes]:
                results.append(item)
        return results
    
    def add_motionpicture(self, mp:MotionPicture):
        if mp not in self.search(mp.title, key="title"):  # type comparison is in inside the proper class
            self.collection.append(mp)
    
    def add_season(self, series:Series):
        """Add the whole Series season to the library. The `episode` value indicates the last episode number."""
        for episode in range(1, series.episode+1):
            series.episode = episode
            self.add_motionpicture(series)  # checks for duplicates

    def get_movies(self) -> list[MotionPicture]:
        return sorted([item for item in self.collection if isinstance(item, Movie)], key=lambda x: x.title)

    def get_series(self) -> list[MotionPicture]:
        return sorted([item for item in self.collection if isinstance(item, Series)], key=lambda x: x.title)
    
    def get_series_episodes(self, title, season=0):
        count = 0
        if season > 0:
            for item in self.get_series():
                if (title == item.title
                    and season == item.season):
                    count += 1
        else:
            for item in self.get_series():
                if title == item.title:
                    count += 1
        return count

    def generate_views(self):
        if not self.collection:  # ignore empty library
            return
        movie = random.choice(self.collection)
        views_to_add = random.randint(1, 100)
        movie.views += views_to_add
    
    def generate_views_multiple(self, times=10):
        for _ in range(times):
            self.generate_views()

    def top_titles(self, n=3) -> list[MotionPicture]:
        sorted_collection = sorted(self.collection, key=lambda x: x.views, reverse=True)
        return sorted_collection[:n]
    
if __name__ == "__main__":
    print("Biblioteka filmów")
    library = MovieLibrary()
    library.add_motionpicture(Movie("Inception", 2010, "Sci-Fi"))
    library.add_motionpicture(Series("Wiedźmin", 2019, "Fantasy", 1, 1))
    library.add_motionpicture(Series("Wiedźmin", 2019, "Fantasy", 2, 1))
    library.add_motionpicture(Movie("Pulp Fiction", 1994, "Gangster"))
    library.add_season(Series("Stranger Things", 2016, "Sci-Fi", 1, 8))

    library.generate_views_multiple(20)

    now = datetime.datetime.now().date()
    print(f"Najpopularniejsze filmy i seriale dnia {now.day:02}.{now.month:02}.{now.year}")
    for t in library.top_titles():
        print(f"{t.title} - {t.views} wyświetleń")