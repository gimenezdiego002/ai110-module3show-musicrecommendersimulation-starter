"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


USER_PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Conflicting Classical": {
        "favorite_genre": "classical",
        "favorite_mood": "aggressive",
        "target_energy": 0.95,
        "likes_acoustic": True,
    },
}


def main() -> None:
    """Run recommendations for several normal and adversarial profiles."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in USER_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n=== {profile_name} ===")
        print(
            "User profile: "
            f"genre={user_prefs['favorite_genre']}, "
            f"mood={user_prefs['favorite_mood']}, "
            f"energy={user_prefs['target_energy']}, "
            f"likes_acoustic={user_prefs['likes_acoustic']}"
        )
        print("Top 5 recommendations:\n")
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} by {song['artist']}")
            print(f"   Score: {score:.2f}")
            print(f"   Reasons: {explanation}")
            print()


if __name__ == "__main__":
    main()
