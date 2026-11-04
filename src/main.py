"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import sys

from src.recommender import load_songs, recommend_songs, score_song, STRATEGIES, DEFAULT_STRATEGY

WIDTH = 64

# Three distinct listener types, with every preference filled in
USER_PROFILES = {
    "High-Energy Pop": {
        "genres": ["pop", "indie pop"],
        "moods": ["happy", "euphoric"],
        "artists": ["Max Pulse"],
        "energy": 0.90,
        "valence": 0.85,
        "danceability": 0.85,
        "acousticness": 0.10,
    },
    "Chill Lofi": {
        "genres": ["lofi", "ambient"],
        "moods": ["chill", "focused"],
        "artists": ["LoRoom"],
        "energy": 0.35,
        "valence": 0.60,
        "danceability": 0.55,
        "acousticness": 0.85,
    },
    "Deep Intense Rock": {
        "genres": ["rock", "metal"],
        "moods": ["intense", "aggressive"],
        "artists": ["Voltline"],
        "energy": 0.92,
        "valence": 0.35,
        "danceability": 0.55,
        "acousticness": 0.08,
    },
}

# Edge-case profiles meant to trick the scoring logic.
# Each entry: (user_prefs, k, strategy name or None for the default)
ADVERSARIAL_PROFILES = {
    "Empty profile":                   ({}, 5, None),
    "Out-of-range energy (5.0)":       ({"genre": "pop", "energy": 5.0}, 5, None),
    "NaN energy":                      ({"genre": "lofi", "energy": float("nan")}, 5, None),
    "Genres as a string, not a list":  ({"genres": "pop", "energy": 0.8}, 5, None),
    "Negative k (-1)":                 ({"genre": "pop"}, -1, None),
    "Unknown genre (k-pop)":           ({"genre": "k-pop", "mood": "happy", "energy": 0.8}, 5, None),
    "Trailing space ('Pop ')":         ({"genre": "Pop ", "mood": "happy"}, 5, None),
    "Conflict: metal + peaceful":      ({"genre": "metal", "mood": "peaceful",
                                         "energy": 0.1, "acousticness": 0.95}, 5, None),
    "Synonym mood (sad vs melancholic)": ({"genre": "blues", "mood": "sad", "energy": 0.35},
                                          5, "mood_first"),
    "Artist only (Neon Echo)":         ({"artists": ["Neon Echo"]}, 5, None),
    "Third genre ignored":             ({"genres": ["lofi", "pop", "rock"]}, 5, None),
}


def print_songs(songs) -> None:
    """Prints every song in the catalog as a table."""
    print(f"\n=== Loaded {len(songs)} songs ===\n")
    print(f"{'ID':<4} {'Title':<24} {'Artist':<18} {'Genre':<10} {'Mood':<12} "
          f"{'Energy':>6} {'Tempo':>6} {'Valence':>7} {'Dance':>6} {'Acoustic':>8}")
    print("-" * 113)
    for song in songs:
        print(f"{song['id']:<4} {song['title']:<24} {song['artist']:<18} {song['genre']:<10} {song['mood']:<12} "
              f"{song['energy']:>6.2f} {song['tempo_bpm']:>6.0f} {song['valence']:>7.2f} "
              f"{song['danceability']:>6.2f} {song['acousticness']:>8.2f}")


def print_profile(name, user_prefs) -> None:
    """Prints the user's input preferences."""
    print("\n" + "#" * WIDTH)
    print(f" USER PROFILE: {name.upper()}")
    print("=" * WIDTH)
    for key, value in user_prefs.items():
        if isinstance(value, list):
            value = ", ".join(value)
        print(f"   {key:<14} {value}")


def score_bar(score: float, length: int = 20) -> str:
    """Turns a 0-10 score into a bar like ████████████░░░░░░░░."""
    filled = round(score / 10 * length)
    return "█" * filled + "░" * (length - filled)


def print_rankings(strategy, recommendations, user_prefs) -> None:
    """Prints each recommended song as a card: title, final score, and reasons."""
    print("\n" + "=" * WIDTH)
    print(f" {strategy.name.upper().replace('_', ' ')} STRATEGY")
    print(f" {strategy.description}")
    print("=" * WIDTH)

    for rank, (song, score, _) in enumerate(recommendations, start=1):
        _, reasons = score_song(user_prefs, song, strategy)

        print(f"\n #{rank}  {song['title']:<40} {score:>5.2f} / 10")
        print(f"     {song['artist']} · {song['genre']} · {song['mood']}")
        print(f"     {score_bar(score)}")
        if reasons:
            for reason in reasons:
                print(f"       ✓ {reason}")
        else:
            print("       – no strong matches")

    print("\n" + "-" * WIDTH)


def print_comparison(results_by_strategy, k: int) -> None:
    """Prints the top k titles for every strategy side by side."""
    names = list(results_by_strategy)
    print("\n=== Strategy comparison ===\n")
    print(f"{'Rank':<5} " + " ".join(f"{name:<22}" for name in names))
    print("-" * (6 + 23 * len(names)))
    for i in range(k):
        row = [results_by_strategy[name][i][0]["title"] for name in names]
        print(f"{'#' + str(i + 1):<5} " + " ".join(f"{title:<22}" for title in row))


def run_adversarial(songs) -> None:
    """Runs each edge-case profile and prints its results as a compact table."""
    print("\n" + "#" * WIDTH)
    print(" ADVERSARIAL / EDGE-CASE PROFILES")
    print("#" * WIDTH)

    for name, (user_prefs, k, strategy) in ADVERSARIAL_PROFILES.items():
        label = strategy or DEFAULT_STRATEGY
        print(f"\n== {name}  [k={k}, {label}] ==")
        print(f"   prefs: {user_prefs}")
        try:
            results = recommend_songs(user_prefs, songs, k=k, strategy=strategy)
        except Exception as error:  # show the crash instead of stopping the run
            print(f"   CRASH: {type(error).__name__}: {error}")
            continue

        print(f"   returned {len(results)} song(s)")
        for rank, (song, score, explanation) in enumerate(results, start=1):
            print(f"   #{rank:<3}{score:>7.2f}  {song['title']:<22} "
                  f"{song['genre']:<10} {song['mood']:<12}")
            print(f"         {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")

    # `python -m src.main adversarial` runs only the edge cases
    if "adversarial" in sys.argv[1:]:
        run_adversarial(songs)
        return

    print_songs(songs)
    k = 5

    for name, user_prefs in USER_PROFILES.items():
        print_profile(name, user_prefs)

        # Run the user through every strategy; show full cards for the default one
        results_by_strategy = {}
        for strategy in STRATEGIES.values():
            recommendations = recommend_songs(user_prefs, songs, k=k, strategy=strategy)
            results_by_strategy[strategy.name] = recommendations
            if strategy.name == DEFAULT_STRATEGY:
                print_rankings(strategy, recommendations, user_prefs)

        print_comparison(results_by_strategy, k)


if __name__ == "__main__":
    main()
