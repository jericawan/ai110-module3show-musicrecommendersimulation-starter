"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, score_song, STRATEGIES

WIDTH = 64


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


def print_profile(user_prefs) -> None:
    """Prints the user's input preferences."""
    print("\n" + "=" * WIDTH)
    print(" USER PROFILE")
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


def main() -> None:
    songs = load_songs("data/songs.csv")
    print_songs(songs)
    k = 5

    # Default profile: pop / happy
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.8,
        "danceability": 0.8,
        "acousticness": 0.2,
    }
    print_profile(user_prefs)

    # Run the same user through every weighting strategy to compare rankings
    results_by_strategy = {}
    for strategy in STRATEGIES.values():
        recommendations = recommend_songs(user_prefs, songs, k=k, strategy=strategy)
        results_by_strategy[strategy.name] = recommendations
        print_rankings(strategy, recommendations, user_prefs)

    print_comparison(results_by_strategy, k)


if __name__ == "__main__":
    main()
