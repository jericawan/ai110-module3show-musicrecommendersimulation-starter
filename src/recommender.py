import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    second_genre: Optional[str] = None
    second_mood: Optional[str] = None
    favorite_artists: List[str] = field(default_factory=list)
    target_valence: Optional[float] = None
    target_danceability: Optional[float] = None

    def to_prefs(self) -> Dict:
        """Converts the profile into the dict format used by score_song."""
        genres = [self.favorite_genre] + ([self.second_genre] if self.second_genre else [])
        moods = [self.favorite_mood] + ([self.second_mood] if self.second_mood else [])
        return {
            "genres": genres,
            "moods": moods,
            "artists": self.favorite_artists,
            "energy": self.target_energy,
            "valence": self.target_valence,
            "danceability": self.target_danceability,
            "acousticness": 0.8 if self.likes_acoustic else 0.2,
        }


# ---------------------------------------------------------------------------
# Point weighting strategies
# ---------------------------------------------------------------------------
# Every category is first scored 0-10 on how well the song fits the user.
# A strategy decides how much each category counts toward the final score.
# The final score is a weighted average, so it always stays on a 0-10 scale
# and scores from different strategies can be compared directly.

@dataclass(frozen=True)
class WeightingStrategy:
    """A named set of weights for the four scoring categories."""
    name: str
    description: str
    genre: float
    vibe: float
    artist: float
    mood: float

    def weights(self) -> Dict[str, float]:
        """Returns the weights as a {category: weight} dict."""
        return {"genre": self.genre, "vibe": self.vibe, "artist": self.artist, "mood": self.mood}


STRATEGIES: Dict[str, WeightingStrategy] = {
    "balanced": WeightingStrategy(
        name="balanced",
        description="Genre leads, with vibe, artist, and mood as supporting signals.",
        genre=4.0, vibe=2.5, artist=2.0, mood=1.5,
    ),
    "mood_first": WeightingStrategy(
        name="mood_first",
        description="Matches how the user wants to feel, regardless of genre.",
        genre=1.5, vibe=3.0, artist=1.0, mood=4.5,
    ),
    "vibe_first": WeightingStrategy(
        name="vibe_first",
        description="Matches the sound (energy, valence, danceability, acousticness).",
        genre=1.5, vibe=5.0, artist=1.0, mood=2.5,
    ),
    "discovery": WeightingStrategy(
        name="discovery",
        description="Ignores favorite artists and leans on vibe to surface new music.",
        genre=1.0, vibe=4.0, artist=0.0, mood=3.0,
    ),
}

DEFAULT_STRATEGY = "balanced"

# Numeric features compared for the "vibe" category (all on a 0-1 scale)
VIBE_FEATURES = ["energy", "valence", "danceability", "acousticness"]

# Points for a genre or mood match: first favorite gets full credit, second gets partial
TOP_PICK_POINTS = 10.0
SECOND_PICK_POINTS = 6.0


def get_strategy(strategy: "str | WeightingStrategy | None") -> WeightingStrategy:
    """Looks up a strategy by name, or passes a WeightingStrategy through."""
    if strategy is None:
        return STRATEGIES[DEFAULT_STRATEGY]
    if isinstance(strategy, WeightingStrategy):
        return strategy
    if strategy not in STRATEGIES:
        raise ValueError(f"Unknown strategy '{strategy}'. Options: {', '.join(STRATEGIES)}")
    return STRATEGIES[strategy]


def _top_two(user_prefs: Dict, key: str) -> List[str]:
    """
    Reads a ranked list like 'genres' or 'moods' (top two only), or falls back
    to a single 'genre' / 'mood' value.
    """
    picks = user_prefs.get(key + "s") or []
    if not picks and user_prefs.get(key):
        picks = [user_prefs[key]]
    return [p.lower() for p in picks[:2]]


def score_genre(user_prefs: Dict, song: Dict) -> Tuple[float, Optional[str]]:
    """10 points for the user's top genre, 6 for their second, else 0."""
    genres = _top_two(user_prefs, "genre")
    song_genre = song["genre"].lower()
    if genres and song_genre == genres[0]:
        return TOP_PICK_POINTS, f"matches your top genre ({song['genre']})"
    if song_genre in genres[1:]:
        return SECOND_PICK_POINTS, f"matches your second genre ({song['genre']})"
    return 0.0, None


def score_mood(user_prefs: Dict, song: Dict) -> Tuple[float, Optional[str]]:
    """10 points for the user's top mood, 6 for their second, else 0."""
    moods = _top_two(user_prefs, "mood")
    song_mood = song["mood"].lower()
    if moods and song_mood == moods[0]:
        return TOP_PICK_POINTS, f"has your top mood ({song['mood']})"
    if song_mood in moods[1:]:
        return SECOND_PICK_POINTS, f"has your second mood ({song['mood']})"
    return 0.0, None


def score_artist(user_prefs: Dict, song: Dict) -> Tuple[float, Optional[str]]:
    """10 points if the song is by one of the user's favorite artists, else 0."""
    artists = [a.lower() for a in user_prefs.get("artists") or []]
    if song["artist"].lower() in artists:
        return 10.0, f"is by {song['artist']}, one of your favorite artists"
    return 0.0, None


def score_vibe(user_prefs: Dict, song: Dict) -> Tuple[float, Optional[str]]:
    """10 points minus the average distance from the user's targets (0-1 features)."""
    diffs = [
        abs(float(song[f]) - user_prefs[f])
        for f in VIBE_FEATURES
        if user_prefs.get(f) is not None
    ]
    if not diffs:
        return 0.0, None
    points = 10.0 * (1.0 - sum(diffs) / len(diffs))
    if points >= 8.0:
        return points, "closely matches the vibe you like"
    if points >= 6.0:
        return points, "is fairly close to the vibe you like"
    return points, None


CATEGORY_SCORERS = {
    "genre": score_genre,
    "vibe": score_vibe,
    "artist": score_artist,
    "mood": score_mood,
}


def filled_categories(user_prefs: Dict) -> List[str]:
    """Returns the categories the user actually gave a preference for."""
    filled = {
        "genre": bool(_top_two(user_prefs, "genre")),
        "vibe": any(user_prefs.get(f) is not None for f in VIBE_FEATURES),
        "artist": bool(user_prefs.get("artists")),
        "mood": bool(_top_two(user_prefs, "mood")),
    }
    return [category for category in CATEGORY_SCORERS if filled[category]]


def score_song(
    user_prefs: Dict, song: Dict, strategy: "str | WeightingStrategy | None" = None
) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Algorithm (from the README):
      1. Score each category 0-10 on how close the song is to the user's target:
           genre  - 10 for top genre, 6 for second genre, else 0
           vibe   - 10 minus the average gap on energy, valence,
                    danceability, and acousticness
           artist - 10 if it's a favorite artist, else 0
           mood   - 10 for top mood, 6 for second mood, else 0
      2. Combine them with the strategy's weights
         (balanced: 4.0 genre + 2.5 vibe + 2.0 artist + 1.5 mood).
      3. Divide by the total weight so the final score stays 0-10.

    Categories the user left blank (e.g. no favorite artists) are left out of
    the equation entirely, so they don't drag every song's score down.

    Returns (score, reasons), where reasons explain each strong match.
    """
    weights = get_strategy(strategy).weights()
    categories = filled_categories(user_prefs)
    total_weight = sum(weights[category] for category in categories)

    weighted_points = 0.0
    reasons = []
    for category in categories:
        points, reason = CATEGORY_SCORERS[category](user_prefs, song)
        weighted_points += weights[category] * points
        if reason and weights[category] > 0:
            reasons.append(reason)

    score = weighted_points / total_weight if total_weight else 0.0
    return score, reasons


# Scores this close (the 2 decimals shown to the user) count as a tie
TIE_PRECISION = 2


def rank_key(user_prefs: Dict, song: Dict, score: float, reasons: List[str]) -> Tuple:
    """
    Sort key for ranking, best song first. Ties on score are broken by:
      1. more categories matched (a broader fit)
      2. closer vibe match
      3. title A-Z, so the order is always the same
    """
    vibe_points, _ = score_vibe(user_prefs, song)
    return (-round(score, TIE_PRECISION), -len(reasons), -vibe_points, song["title"].lower())


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song], strategy: "str | WeightingStrategy | None" = None):
        """Stores the song catalog and the weighting strategy to rank with."""
        self.songs = songs
        self.strategy = get_strategy(strategy)

    def set_strategy(self, strategy: "str | WeightingStrategy") -> None:
        """Switches to a different weighting strategy."""
        self.strategy = get_strategy(strategy)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the user's top k songs, best first."""
        songs_by_id = {song.id: song for song in self.songs}
        song_dicts = [asdict(song) for song in self.songs]
        results = recommend_songs(user.to_prefs(), song_dicts, k, self.strategy)
        return [songs_by_id[song["id"]] for song, _, _ in results]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a sentence explaining why the song fits the user."""
        score, reasons = score_song(user.to_prefs(), asdict(song), self.strategy)
        return _format_explanation(score, reasons, self.strategy)


def _format_explanation(score: float, reasons: List[str], strategy: WeightingStrategy) -> str:
    """Joins the reasons into one readable sentence."""
    if not reasons:
        return f"Scored {score:.2f}/10 ({strategy.name}), but no strong matches."
    return f"This song {'; '.join(reasons)} ({strategy.name} weighting)."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            song = {}
            for column, value in row.items():
                try:
                    song[column] = float(value)
                except ValueError:
                    song[column] = value  # text fields like title, genre, mood
            # id is an identifier, not a measurement, so keep it a whole number
            song["id"] = int(song["id"])
            songs.append(song)
    return songs


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    strategy: "str | WeightingStrategy | None" = None,
) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    1. Score every song with score_song.
    2. Rank them from highest to lowest score (ties broken by rank_key).
    3. Return the top k as (song, score, explanation).
    """
    chosen = get_strategy(strategy)

    # Step 1: score every song once
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, chosen)
        scored.append((song, score, reasons))

    # Step 2: rank, best first
    scored.sort(key=lambda item: rank_key(user_prefs, item[0], item[1], item[2]))

    # Step 3: keep the top k and turn the reasons into a sentence
    return [
        (song, score, _format_explanation(score, reasons, chosen))
        for song, score, reasons in scored[:k]
    ]
