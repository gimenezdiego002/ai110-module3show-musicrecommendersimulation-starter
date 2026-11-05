# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real streaming platforms build a representation of a listener's taste from
behavioral data such as plays, completion rate, skips, likes, saves, searches,
playlist additions, and listening history. They can combine **collaborative
filtering**, which recommends music enjoyed by people with behavior similar to
the current listener, with **content-based filtering**, which compares the
attributes of songs to the listener's preferences. Spotify also describes
using context and trends, while YouTube describes a two-stage process that
first generates possible recommendations and then ranks them. This simulation
uses the simpler content-based approach: it prioritizes genre and mood matches,
then rewards songs whose energy is close to the user's target and whose
acousticness fits the user's preference.

### Features

- A `Song` stores `id`, `title`, `artist`, `genre`, `mood`, `energy`,
  `tempo_bpm`, `valence`, `danceability`, and `acousticness` from
  `data/songs.csv`.
- A `UserProfile` stores `favorite_genre`, `favorite_mood`, `target_energy`,
  and `likes_acoustic`.
- The first scoring recipe uses `genre`, `mood`, `energy`, and `acousticness`.
  Tempo, valence, and danceability are useful future additions because they
  help describe pace, emotional positivity, and movement, but using every
  available field immediately would make a small recommender harder to explain
  and tune.

### Algorithm Recipe

For each song, the recommender adds 3 points for a matching genre and 2 points
for a matching mood. Energy is a closeness score rather than a "higher is
better" score: `energy_match = 1 - abs(song.energy - user.target_energy)`.
Because both values are between 0 and 1, this gives 1 for a perfect match and
approaches 0 as the values move apart; multiplying it by 2 gives energy up to 2
points. Acoustic preference contributes up to 1 additional point. Genre is
weighted most heavily because it usually defines the broad musical style,
while mood and energy refine the desired vibe.

The **scoring rule** evaluates one song against one profile and produces a
comparable number. The **ranking rule** applies that scoring rule to every song,
sorts the results from highest to lowest score, and returns the top `k` songs.
Both are necessary: a score measures fit, while ranking turns many individual
measurements into an ordered recommendation list.

The implementation uses `sorted()` so it creates a new ranked list and leaves
the original catalog unchanged. In contrast, a list's `.sort()` method would
reorder that list in place and return `None`.

### Example User Profile

```python
user_prefs = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.85,
    "likes_acoustic": False,
}
```

This profile separates "intense rock" from "chill lofi": genre and mood
describe the style, high target energy captures intensity, and the acoustic
preference gives a further contrast (lofi tracks are highly acoustic).

### Scoring Summary

```
Genre match:       +3.0
Mood match:        +2.0
Energy similarity: up to +2.0   (2.0 * (1 - abs(song_energy - target_energy)))
Acoustic fit:      up to +1.0
```

Mood and energy together (up to 4.0) can outweigh a genre match (3.0), so a
song with the right vibe can compete despite a different genre.

### Data Flow

```
User preferences
       ↓
Load every song from songs.csv
       ↓
Score each song independently
       ↓
Sort songs by score
       ↓
Return the top K recommendations
```

### Expected Biases

- Over-prioritizes exact genre and mood labels, so near-matches (e.g. "indie
  pop" vs "pop") get no genre credit.
- Misses good cross-genre recommendations.
- Treats musical taste as fixed instead of contextual (workout vs. studying).
- Favors categories represented by more songs (lofi has 3 entries; many genres
  have only 1).
- Oversimplifies acoustic preference into a yes/no value.

### Research Sources

- [Spotify: Understanding recommendations](https://www.spotify.com/safetyandprivacy/understanding-recommendations)
- [Spotify Engineering: Humans + Machines](https://engineering.atspotify.com/2023/04/humans-machines-a-look-behind-spotifys-algotorial-playlists)
- [Google Research: Deep Neural Networks for YouTube Recommendations](https://research.google.com/pubs/archive/45530.pdf)

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```text
Loaded songs: 17
User profile: genre=pop, mood=happy, energy=0.8, likes_acoustic=False

Top 5 recommendations:

1. Sunrise City by Neon Echo
   Score: 7.78
   Reasons: genre match (+3.00); mood match (+2.00); energy similarity (+1.96); non-acoustic fit (+0.82)

2. Gym Hero by Max Pulse
   Score: 5.69
   Reasons: genre match (+3.00); energy similarity (+1.74); non-acoustic fit (+0.95)

3. Rooftop Lights by Indigo Parade
   Score: 4.57
   Reasons: mood match (+2.00); energy similarity (+1.92); non-acoustic fit (+0.65)

4. Crown Me by Verse Kingdom
   Score: 2.84
   Reasons: energy similarity (+1.96); non-acoustic fit (+0.88)

5. Calle Fuego by Los Vientos
   Score: 2.76
   Reasons: energy similarity (+1.84); non-acoustic fit (+0.92)
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



