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


def main() -> None:
    songs = load_songs("data/songs.csv")

    # User taste profile — target values for content-based scoring
    user_prefs = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.40,
        "valence": 0.60,
        "acousticness": 0.75,
        "tempo_bpm": 78,
        "likes_acoustic": True,
    }

    print("=" * 60)
    print("  USER PROFILE")
    print("=" * 60)
    print(f"  Genre: {user_prefs['genre']:<12s}  Mood: {user_prefs['mood']}")
    print(f"  Energy: {user_prefs['energy']:<11.2f}  Valence: {user_prefs['valence']:.2f}")
    print(f"  Acousticness: {user_prefs['acousticness']:<5.2f}  Tempo: {user_prefs['tempo_bpm']:.0f} bpm")
    print("=" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n  TOP {len(recommendations)} RECOMMENDATIONS (out of {len(songs)} songs)")
    print("=" * 60)

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


if __name__ == "__main__":
    main()
