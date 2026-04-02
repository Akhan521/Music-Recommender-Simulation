from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
    target_valence: float = 0.60
    target_acousticness: float = 0.50
    target_tempo_bpm: float = 100.0

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Scores all songs against the user profile and returns the top-k
        songs sorted by score descending.

        Args:
            user: A UserProfile containing taste preferences.
            k: Number of top recommendations to return (default 5).

        Returns:
            A list of up to k Song objects, highest-scoring first.
        """
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Generates a human-readable explanation of why a song was
        recommended for a given user profile.

        Args:
            user: The user's taste preferences.
            song: The song being explained.

        Returns:
            A string describing which features matched or missed
            and how many points each contributed.
        """
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns a list of dictionaries.

    Each row becomes a dict keyed by column header. Numeric fields
    (id, energy, tempo_bpm, valence, danceability, acousticness) are
    cast to int or float so they can be used in scoring math.

    Args:
        csv_path: Path to the CSV file (absolute or relative to project root).

    Returns:
        A list of song dictionaries with typed values.
    """
    import csv

    numeric_fields = {"id": int, "energy": float, "tempo_bpm": float,
                      "valence": float, "danceability": float, "acousticness": float}
    import os
    if not os.path.isabs(csv_path) and not os.path.exists(csv_path):
        # Resolve relative to project root (one level up from src/)
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base, csv_path)

    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field, cast in numeric_fields.items():
                row[field] = cast(row[field])
            songs.append(row)

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

TEMPO_RANGE = 108  # max BPM (168) - min BPM (60) in our catalog


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Returns:
        (score, reasons) where score is 0.0–10.0 and reasons is a list
        of human-readable strings explaining each scoring component.
    """
    score = 0.0
    reasons = []

    # --- Categorical features (binary match) ---

    # Genre match: +3.0
    if user_prefs["genre"] == song["genre"]:
        score += 3.0
        reasons.append(f"genre matched ({song['genre']}): +3.00")
    else:
        reasons.append(f"genre mismatch ({song['genre']} != {user_prefs['genre']}): +0.00")

    # Mood match: +2.0
    if user_prefs["mood"] == song["mood"]:
        score += 2.0
        reasons.append(f"mood matched ({song['mood']}): +2.00")
    else:
        reasons.append(f"mood mismatch ({song['mood']} != {user_prefs['mood']}): +0.00")

    # --- Numerical features (closeness scoring) ---

    # Energy: (1 - |diff|) × 2.5
    energy_closeness = 1 - abs(user_prefs["energy"] - song["energy"])
    energy_pts = energy_closeness * 2.5
    score += energy_pts
    reasons.append(f"energy closeness ({song['energy']:.2f} vs {user_prefs['energy']:.2f}): +{energy_pts:.2f}")

    # Valence: (1 - |diff|) × 1.0
    valence_closeness = 1 - abs(user_prefs["valence"] - song["valence"])
    valence_pts = valence_closeness * 1.0
    score += valence_pts
    reasons.append(f"valence closeness ({song['valence']:.2f} vs {user_prefs['valence']:.2f}): +{valence_pts:.2f}")

    # Acousticness: (1 - |diff|) × 1.0
    acousticness_closeness = 1 - abs(user_prefs["acousticness"] - song["acousticness"])
    acousticness_pts = acousticness_closeness * 1.0
    score += acousticness_pts
    reasons.append(f"acousticness closeness ({song['acousticness']:.2f} vs {user_prefs['acousticness']:.2f}): +{acousticness_pts:.2f}")

    # Tempo: (1 - |diff| / TEMPO_RANGE) × 0.5
    tempo_closeness = 1 - abs(user_prefs["tempo_bpm"] - song["tempo_bpm"]) / TEMPO_RANGE
    tempo_pts = max(tempo_closeness, 0) * 0.5  # clamp to 0 if diff exceeds range
    score += tempo_pts
    reasons.append(f"tempo closeness ({song['tempo_bpm']:.0f} vs {user_prefs['tempo_bpm']:.0f} bpm): +{tempo_pts:.2f}")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Scores every song, sorts by score descending, returns top-k as
    (song_dict, score, explanation) tuples.
    """
    scored = sorted(
        (
            (song, total, "; ".join(reasons))
            for song in songs
            for total, reasons in [score_song(user_prefs, song)]
        ),
        key=lambda x: x[1],
        reverse=True,
    )
    return scored[:k]
