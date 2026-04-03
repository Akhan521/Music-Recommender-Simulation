"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs


def print_profile(label: str, prefs: dict, songs: list) -> None:
    """Print a single user profile and its top-5 recommendations."""
    print("\n" + "=" * 60)
    print(f"  PROFILE: {label}")
    print("=" * 60)
    print(f"  Genre: {prefs['genre']:<12s}  Mood: {prefs['mood']}")
    print(f"  Energy: {prefs['energy']:<11.2f}  Valence: {prefs['valence']:.2f}")
    print(f"  Acousticness: {prefs['acousticness']:<5.2f}  Tempo: {prefs['tempo_bpm']:.0f} bpm")
    print("=" * 60)

    recommendations = recommend_songs(prefs, songs, k=5)

    print(f"\n  TOP {len(recommendations)} RECOMMENDATIONS (out of {len(songs)} songs)")
    print("-" * 60)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar_length = int(score / 10 * 30)
        bar = "#" * bar_length + "-" * (30 - bar_length)

        print(f"\n  #{rank}  {song['title']}")
        print(f"       Artist: {song['artist']}  |  Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"       Score:  {score:.2f} / 10.00  [{bar}]")
        print(f"       Breakdown:")
        for reason in explanation.split("; "):
            print(f"         - {reason}")
    print("\n" + "=" * 60)


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = {
        # 1. Baseline — the original chill lo-fi listener
        "Chill Lo-Fi Listener": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.40,
            "valence": 0.60,
            "acousticness": 0.75,
            "tempo_bpm": 78,
            "likes_acoustic": True,
        },
        # 2. Adversarial — high energy contradicts sad mood;
        #    tests whether numeric closeness can overpower a mood
        #    mismatch and surface unexpected picks
        "EDGE: High Energy + Sad Mood": {
            "genre": "country",
            "mood": "sad",
            "energy": 0.95,
            "valence": 0.20,
            "acousticness": 0.50,
            "tempo_bpm": 100,
            "likes_acoustic": True,
        },
        # 3. Adversarial — genre & mood that don't exist in our
        #    catalog; every song gets +0 for both categorical
        #    features, so ranking depends entirely on numeric
        #    closeness — exposes whether the algorithm degrades
        #    gracefully or produces nonsensical results
        "EDGE: Nonexistent Genre & Mood": {
            "genre": "reggaeton",
            "mood": "dreamy",
            "energy": 0.50,
            "valence": 0.50,
            "acousticness": 0.50,
            "tempo_bpm": 100,
            "likes_acoustic": True,
        },
    }

    for label, prefs in profiles.items():
        print_profile(label, prefs, songs)


if __name__ == "__main__":
    main()
