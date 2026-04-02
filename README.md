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

Real-world recommenders like Spotify and YouTube combine two broad strategies: collaborative filtering, which finds patterns across millions of users' behaviors to suggest what similar listeners enjoyed, and content-based filtering, which analyzes the attributes of songs a user already likes to find more of the same. Production systems blend both approaches with deep learning, processing billions of implicit signals (plays, skips, listen duration) to generate candidates, rank them, and re-rank for diversity.

Our simulation focuses on the content-based side. Each `Song` carries six scorable features: `genre`, `mood`, `energy`, `valence`, `acousticness`, and `tempo_bpm`. A `UserProfile` stores a preferred genre, mood, target energy level, target valence, target acousticness, target tempo, and an acoustic preference flag.

### Algorithm Recipe

The `Recommender` scores every song on a **0 to 10 point scale** using this formula:

**Categorical features** (binary match — full points or zero):

| Feature | Points | Why this weight |
|---|---|---|
| Genre match | +3.0 | Strongest signal — defines the sonic identity (instruments, production, structure) |
| Mood match | +2.0 | Distinguishes *when* a song fits; two lofi tracks can serve very different moments |

**Numerical features** (closeness — `(1 - |user_target - song_value|) × weight`):

| Feature | Max points | Why this weight |
|---|---|---|
| Energy | ×2.5 | Core vibe axis — the single largest feel difference between songs in the catalog |
| Valence | ×1.0 | Emotional tone — separates brooding from bright within similar energy ranges |
| Acousticness | ×1.0 | Production texture — acoustic coffee-shop feel vs. electronic club feel |
| Tempo | ×0.5 | Weakest solo signal; normalized by BPM range (60–168 = 108 span) to prevent raw BPM gaps from dominating |

**Score budget**: categorical features control 50% of the ceiling (5.0 pts), numerical features control the other 50% (5.0 pts). A perfect genre + mood match gets a song halfway; the numerical closeness scores decide the final ranking among categorical peers.

**Ranking**: after all songs are scored, sort descending and return the top-k (default 5).

### Expected Biases and Limitations

- **Genre dominance**: at 3.0 points (30% of max score), genre is the heaviest single feature. A non-matching genre song needs near-perfect scores on every other dimension to compete with even a mediocre genre match. This creates a filter-bubble effect — a lofi listener will rarely see jazz recommendations even when the jazz track's energy, valence, and acousticness are a closer fit.
- **Mood rigidity**: mood is categorical (match or miss), but real moods exist on a spectrum. "Chill" and "relaxed" feel similar to a listener, yet our system treats them as completely different, awarding zero points for a near-miss.
- **No discovery mechanism**: the system only rewards closeness to existing preferences. It has no way to introduce variety or surprise, which real recommenders handle through exploration strategies and diversity re-ranking.
- **Single-profile assumption**: the system models each user as having one fixed taste. Real listeners shift between moods (workout vs. sleep vs. focus), but our profile has no context awareness.
- **Small catalog bias**: with only 20 songs and 11 genres, most genres have 1–2 representatives. A genre match filter effectively pre-selects 1–2 songs, giving the numerical features very little ranking work to do.

### Sample Output

Below is the terminal output from running the recommender with a lofi/chill user profile:

![User profile and #1 recommendation](screenshots/screenshot_1.png)

![#2 Library Rain and #3 Focus Flow](screenshots/screenshot_2.png)

![#4 Spacewalk Thoughts and #5 Coffee Shop Stories](screenshots/screenshot_3.png)

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


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"
