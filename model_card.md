# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**FlowFinder 1.0**

---

## 2. Intended Use

This recommender suggests five songs from a small catalog based on a user's preferred genre, mood, energy level, and a few other audio traits. It assumes one fixed taste profile per user and does not learn or adapt over time.

---

## 3. How the Model Works

Each song has six features the system cares about: genre, mood, energy, valence (how happy or sad it sounds), acousticness (acoustic vs. electronic texture), and tempo. A user profile sets a target value for each of these.

The system scores every song on a scale of 0 to 10. Genre and mood are yes-or-no checks. If the song's genre matches the user's favorite, it gets 3 points. If the mood matches, it gets 2 points. The remaining 5 points come from how close the song's numbers are to what the user wants. Energy matters most (up to 2.5 points), then valence and acousticness (1 point each), and finally tempo (half a point). After scoring all 20 songs, the system sorts them highest to lowest and returns the top five.

We expanded the starter logic by adding valence, acousticness, and tempo as scoring dimensions. The original version only used genre, mood, and energy.

---

## 4. Data

The catalog contains 20 songs stored in a CSV file. There are 14 genres (pop, lofi, rock, jazz, ambient, electronic, hip-hop, r&b, country, classical, metal, folk, synthwave, and indie pop) and 11 moods (happy, chill, intense, focused, relaxed, moody, energetic, romantic, sad, nostalgic, and angry). Most genres have only one or two songs, so a genre match often narrows the field to a very small set.

We expanded the catalog from the original 10 songs to 20 to cover more variety. The dataset still skews toward Western genres and English-language music. Latin, African, Middle Eastern, and Asian music traditions are not represented. There is also no information about lyrics, language, or song length.

---

## 5. Strengths

The system works well when the user's preferences line up with genres that have multiple songs in the catalog. For example, a chill lo-fi listener gets strong results because there are three lofi tracks with different mood and energy profiles, giving the numeric scoring room to differentiate.

The scoring breakdown is fully transparent. Every recommendation comes with a line-by-line explanation showing exactly how many points each feature contributed. This makes it easy to understand why a song was picked and to spot when the logic does something unexpected.

The system also handles missing or unknown inputs gracefully. When we tested a user who asked for "reggaeton" (a genre not in the catalog), it did not crash or return empty results. It fell back to numeric closeness and still returned five songs, even though the recommendations lacked confidence.

---

## 6. Limitations and Bias

When we temporarily disabled the mood check, Focus Flow (mood: focused) jumped from #3 to #1 for a chill lo-fi listener. Midnight Coding and Library Rain, two songs whose "chill" mood had been the only thing keeping them ahead, both dropped. This shows that mood acts more like a blunt gate than a nuanced signal. Songs that match the mood label get a large bonus, while near-miss moods like "focused" or "relaxed" receive zero credit even though they feel similar to "chill" in practice.

The flip side is also a problem. Without mood, the system loses the ability to tell apart *why* a user wants lo-fi (to relax vs. to concentrate). Rankings collapse into pure number-matching, and folk, jazz, and ambient songs end up competing on equal footing with no context.

In the adversarial "High Energy + Sad" profile, disabling mood caused Elegy in D Minor (classical/sad) to fall out of the top 5 entirely. Storm Runner (rock/intense) replaced it. That swap makes sense by the numbers but not by feeling. A user looking for sad music would not want an intense rock track. The core weakness is that mood is too powerful when it matches and too brittle when it nearly matches, creating a filter bubble around exact mood labels while ignoring the emotional range between them.

---

## 7. Evaluation

We tested three user profiles. The first was a **Chill Lo-Fi Listener** as a baseline. The second was a **High Energy + Sad Mood** edge case with conflicting preferences. The third was a **Nonexistent Genre and Mood** edge case using "reggaeton" and "dreamy," labels that do not appear anywhere in the catalog. For each profile we ran the recommender twice: once with mood scoring on, and once with mood scoring off.

The baseline profile gave intuitive results. Midnight Coding and Library Rain ranked #1 and #2 with scores near 9.9 out of 10. The surprise came when we turned mood off. Focus Flow overtook both chill songs for #1 because its energy, acousticness, and tempo were actually a closer fit all along. The +2.0 mood bonus had been masking that.

In the High Energy + Sad profile, Broken Compass held #1 in both runs, but Elegy in D Minor dropped out without its mood bonus. It was replaced by Storm Runner, a track with better energy alignment but no emotional relevance to a sad-music listener.

The nonexistent-genre profile gave identical results in both runs. Since "dreamy" matched nothing, mood was already contributing zero before we disabled it. This served as a useful control to confirm our experiment was only changing one variable.

See [reflection.md](reflection.md) for a per-profile comparison of the mood-on vs. mood-off outputs.

---

## 8. Future Work

Replace the binary mood check with a similarity score. Moods like "chill," "relaxed," and "focused" should be treated as close neighbors instead of completely unrelated labels. One approach is to map moods onto a small number of axes (energy, positivity) and score the distance between them.

Add a diversity penalty so the top five results do not all come from the same genre or artist. Right now, if the catalog had five lofi tracks, a lofi listener could easily get all five back with nothing new to discover.

Support multiple taste profiles per user. A real listener might want high-energy pop for the gym and ambient chill for studying. The system could let users switch between saved profiles or blend them.

Expand the catalog with non-Western genres, different languages, and more songs per genre so that the numeric scoring has a larger pool to work with and recommendations feel less repetitive.

---

## 9. Personal Reflection

Building this system made the "filter bubble" idea feel concrete instead of abstract. It was easy to see how a small scoring rule (like a 2-point mood bonus) can quietly lock a user into a narrow slice of the catalog. Even with only 20 songs, the recommender kept surfacing the same few tracks for each profile while ignoring songs that a real person might enjoy.

The sensitivity experiment was the most revealing part. Removing one feature and watching the rankings shift showed that the system's confidence is fragile. Small weight changes produce big swings, which means the people who design these weights have a lot of hidden influence over what listeners hear. In a real music app with millions of songs, those design choices would be invisible to the user but would shape their entire listening experience.

Using AI tools like Claude Code helped me explore this codebase more smoothly and helped me identify the core sections of each file to work on. I also found it to be a useful tool for debugging and testing the code. If I were to extend this project, I would add support for multiple taste profiles per user, as that I believe is the most natural extension of the project with the most practical use. In our simple use case, we resorted to sorting to produce our top K recommendations. It made me realize that we could still utilize simple algorithms like sorting and produce results that feel like recommendations (using scoring logic to rank the songs and then selecting the top K).
