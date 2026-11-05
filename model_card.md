# Model Card: VibeRank 1.0

## 1. Model Name

**VibeRank 1.0**

The name describes how the system ranks songs by their musical vibe.

---

## 2. Goal / Task

VibeRank suggests songs that may fit a user's taste. It compares each song
with the user's favorite genre, mood, energy level, and acoustic preference.
It returns the five songs with the highest scores. It also explains why each
song received its score.

---

## 3. Data Used

The catalog contains 17 fictional songs. Each song has an ID, title, artist,
genre, mood, energy, tempo, valence, danceability, and acousticness. Energy,
valence, danceability, and acousticness use values from 0.0 to 1.0.

The catalog is small. Lofi has three songs, but many genres have only one.
It has no lyrics, release dates, languages, listening history, likes, or skips.
The data cannot represent the full variety of real music or real listeners.

---

## 4. Algorithm Summary

An exact genre match earns 3 points. An exact mood match earns 2 points. A
song can earn up to 2 points when its energy is close to the user's target.
It can earn up to 1 more point when its acousticness fits the user's choice.

The system scores every song. It then sorts the songs from highest to lowest
score and returns the top five. This is a fixed scoring system. It does not
learn from user behavior.

---

## 5. Observed Behavior / Biases

The system works best when one song matches most of a user's preferences. It
can create a filter bubble because exact genre and mood matches get large
bonuses. Related labels do not count as matches, so `indie pop` gets no genre
points for a `pop` user.

The small catalog also creates an imbalance. Lofi users have several matching
songs, while classical or rock users have only one exact genre match. The
three-point genre bonus can overpower conflicting evidence. For example, a
low-energy classical song ranked first for a user who requested aggressive,
high-energy music.

---

## 6. Evaluation Process

I tested four profiles against all 17 songs:

- High-Energy Pop
- Chill Lofi
- Deep Intense Rock
- Conflicting Classical, an adversarial edge case

The first three results felt reasonable. `Sunrise City`, `Library Rain`, and
`Storm Runner` won their matching profiles. Each song matched the requested
genre and also fit most of the other preferences.

`Sunrise City` ranked first for High-Energy Pop with 7.66 points. It earned
3.00 for genre, 2.00 for mood, 1.84 for energy, and 0.82 for its non-acoustic
fit. This made its first-place ranking easy to explain.

The edge case produced the biggest surprise. `Morning Adagio` ranked first
because its classical genre match outweighed its poor energy and mood fit.
This showed that a high weight can control the result even when other features
disagree.

### Baseline Results

#### High-Energy Pop

```text
User profile: genre=pop, mood=happy, energy=0.9, likes_acoustic=False
1. Sunrise City - 7.66
2. Gym Hero - 5.89
3. Rooftop Lights - 4.37
4. Neon Ascent - 2.96
5. Storm Runner - 2.88
```

#### Chill Lofi

```text
User profile: genre=lofi, mood=chill, energy=0.35, likes_acoustic=True
1. Library Rain - 7.86
2. Midnight Coding - 7.57
3. Focus Flow - 5.68
4. Spacewalk Thoughts - 4.78
5. Porch Light Letters - 2.87
```

#### Deep Intense Rock

```text
User profile: genre=rock, mood=intense, energy=0.9, likes_acoustic=False
1. Storm Runner - 7.88
2. Gym Hero - 4.89
3. Neon Ascent - 2.96
4. Calle Fuego - 2.88
5. Iron Descent - 2.83
```

#### Conflicting Classical

```text
User profile: genre=classical, mood=aggressive, energy=0.95, likes_acoustic=True
1. Morning Adagio - 4.43
2. Iron Descent - 3.99
3. Storm Runner - 2.02
4. Gym Hero - 2.01
5. Rooftop Lights - 1.97
```

### Profile Comparisons

High-Energy Pop and Chill Lofi shared no top-five songs. Their energy and
acoustic preferences pointed in opposite directions. High-Energy Pop and Deep
Intense Rock shared three songs because both requested loud, non-acoustic
music, but their genre and mood bonuses created different winners.

Chill Lofi favored slow and acoustic tracks. Deep Intense Rock favored fast
and non-acoustic tracks. The Conflicting Classical profile split its points
between opposite songs because no song satisfied all of its preferences.

### Why Gym Hero Keeps Showing Up for Happy Pop

`Gym Hero` is a pop song with very high energy and almost no acoustic sound.
A Happy Pop listener who wants lively music gets three things from it: the
pop genre bonus, a close energy match, and a good non-acoustic fit. It only
misses the "happy" mood, since its mood is "intense." That is not enough to
drop it out of the top five. The system does not know that "intense" feels
different from "happy" to a person. It only counts matching labels and
numbers. A bigger catalog with more happy pop songs would push `Gym Hero`
down the list.

### Weight Experiment

I temporarily reduced genre from 3.0 to 1.5 points. I also increased energy
from 2.0 to 4.0 possible points. The normal profiles kept the same winners.
The edge case changed from `Morning Adagio` to `Iron Descent`.

The experiment improved the energy and mood fit for that edge case. However,
it made every list less sensitive to genre. I restored the original weights
because the change was a tradeoff, not a clear overall improvement.

The automated test suite also checks loading, numeric conversion, scoring,
ranking, explanations, and catalog mutation. All five tests pass.

---

## 7. Intended Use and Non-Intended Use

### Intended Use

VibeRank is a classroom simulation. It demonstrates how song features and user
preferences can become scores, explanations, and rankings. It is useful for
learning Python, testing weights, and discussing recommendation bias.

### Non-Intended Use

VibeRank should not power a real music service. It should not be used to judge
artists or predict commercial success. It should not make important decisions
about people. Its small fictional dataset is not evidence about real listeners
or the music industry.

---

## 8. Ideas for Improvement

- Add more songs with balanced coverage across genres and moods.
- Let users select several genres and control the feature weights.
- Learn from likes and skips, then add diversity rules to the final list.

---

## 9. Personal Reflection

My biggest learning moment was seeing how much the weights control the result.
The conflicting classical profile looked strange, but the score explained
exactly why it happened. A simple formula can still feel intelligent when its
inputs describe a person's taste and its output is ranked clearly.

AI tools helped me brainstorm profiles, implement the CSV and ranking logic,
and identify useful edge cases. I still needed to check the generated math,
run the program, compare the output with my own intuition, and confirm that
temporary experiment weights were restored. The explanations and automated
tests were especially useful for checking the AI-assisted work.

I was surprised that a few rules created recommendations that often felt
reasonable. I also learned that a convincing result is not always a fair or
accurate one. If I continued the project, I would add more balanced data,
support multiple tastes, and use listener feedback to adjust recommendations
over time.
