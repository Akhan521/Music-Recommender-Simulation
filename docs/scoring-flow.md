# Scoring & Recommendation Data Flow

```mermaid
flowchart TD
    A["<b>songs.csv</b><br/>20 songs with 10 attributes each"] --> B["<b>Load Songs</b><br/>Parse CSV into list of song dicts"]
    UP["<b>User Profile</b><br/>genre, mood, energy,<br/>valence, acousticness, tempo"] --> D

    B --> C{"<b>For Each Song</b><br/>Loop through all 20 songs"}

    C --> D["<b>Score One Song</b>"]

    D --> D1["<b>Genre Match?</b><br/>lofi == lofi → +3.0<br/>lofi != rock → +0.0"]
    D --> D2["<b>Mood Match?</b><br/>chill == chill → +2.0<br/>chill != intense → +0.0"]
    D --> D3["<b>Energy Closeness</b><br/>(1 - |0.40 - song|) × 2.5"]
    D --> D4["<b>Valence Closeness</b><br/>(1 - |0.60 - song|) × 1.0"]
    D --> D5["<b>Acousticness Closeness</b><br/>(1 - |0.75 - song|) × 1.0"]
    D --> D6["<b>Tempo Closeness</b><br/>(1 - |78 - song| / 108) × 0.5"]

    D1 --> E["<b>Sum All Points</b><br/>total = genre + mood + energy<br/>+ valence + acousticness + tempo"]
    D2 --> E
    D3 --> E
    D4 --> E
    D5 --> E
    D6 --> E

    E --> F["<b>Attach Score + Explanation</b><br/>(song, 9.74, 'genre + mood matched,<br/>energy close')"]

    F --> C

    C -- "All songs scored" --> G["<b>Sort by Score</b><br/>Descending order"]

    G --> H["<b>Return Top K</b><br/>Slice first k songs<br/>(default k=5)"]

    H --> I["<b>Output</b><br/>Ranked list with scores<br/>and explanations"]
```

## How a Single Song Moves Through the Pipeline

1. **Load** — A row in `songs.csv` becomes a dictionary with typed values
2. **Pair** — The song dict meets the user profile dict
3. **Score** — Six independent sub-scores are computed (2 categorical, 4 numerical)
4. **Sum** — Sub-scores combine into a single total (0.0 to 10.0)
5. **Annotate** — The total score and a human-readable explanation are attached
6. **Collect** — The scored song joins all other scored songs in a list
7. **Rank** — The list is sorted by score, highest first
8. **Select** — The top-k songs are sliced off and returned to the caller
