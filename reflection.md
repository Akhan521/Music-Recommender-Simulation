# Reflection: Mood Sensitivity Experiment

We tested what happens when the recommender stops caring about mood entirely. For each profile, we compared the original results (mood on) against the experimental results (mood off).

## Profile 1 — Chill Lo-Fi Listener

With mood on, Midnight Coding ranked #1 because it matched the "chill" label. When we turned mood off, Focus Flow — a "focused" lo-fi track — jumped to #1 instead. Its energy, tempo, and acousticness were actually a closer fit all along, but the mood label had been hiding that. To a real listener, "chill" and "focused" lo-fi feel pretty similar, so the system was arguably wrong to rank Focus Flow lower in the first place.

## Profile 2 — High Energy + Sad Mood

This profile asks for something contradictory: high energy but a sad mood. With mood on, Broken Compass (a slow, sad country song) won because of its "sad" label, even though its energy was way off. With mood off, Ghost of Highway 9 took the lead — it has better tempo alignment and is still a country song. The biggest change was Elegy in D Minor, a quiet classical piece, falling out of the top 5 completely. Its only advantage had been the "sad" label. Storm Runner, a high-energy rock track, replaced it — better energy fit, but not sad at all. This shows the trade-off: mood helps prevent emotionally wrong picks, but it rewards exact label matches instead of understanding that "sad" and "nostalgic" are close in feeling.

## Profile 3 — Nonexistent Genre & Mood

This user asked for "reggaeton" and "dreamy," neither of which exist in our song catalog. The results were identical with mood on or off, which makes sense — mood was already contributing nothing since no song matched "dreamy." All five recommendations scored within a narrow range and felt arbitrary, like the system was guessing. This confirmed that when the recommender has no genre or mood to latch onto, it cannot meaningfully tell songs apart.
