# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

When we temporarily disabled the mood check, Focus Flow (mood: focused) jumped from #3 to #1 for a chill lo-fi listener, overtaking Midnight Coding and Library Rain, two songs whose "chill" mood had been the only thing keeping them ahead. This reveals that mood acts less as a nuanced preference signal and more as a blunt 2-point gate: songs on the right side of the gate get a large, unearned advantage, while near-miss moods like "focused" or "relaxed" receive zero credit despite being experientially close to "chill." The flip side is equally problematic; without mood, the system loses its ability to distinguish *why* a user wants lo-fi (to relax vs. to concentrate), and rankings collapse into pure numeric proximity where Folk, Jazz, and Ambient songs compete on equal footing with no contextual anchor. In the adversarial "High Energy + Sad" profile, disabling mood caused Elegy in D Minor (classical/sad) to fall out of the top 5 entirely, replaced by Storm Runner (rock/intense), a recommendation that makes no emotional sense for a user seeking sad music. The core weakness is that mood is simultaneously too powerful when it matches (a 20% score bonus for a single binary check) and too brittle when it nearly matches (zero partial credit), creating a filter bubble around exact mood labels while ignoring the emotional spectrum between them.

---

## 7. Evaluation  

We tested three user profiles: a **Chill Lo-Fi Listener** (baseline), a **High Energy + Sad Mood** edge case (conflicting preferences), and a **Nonexistent Genre & Mood** edge case (reggaeton/dreamy — labels absent from the catalog). For each profile we ran the recommender with mood scoring enabled, then re-ran with mood disabled to measure sensitivity.

The baseline profile produced intuitive results — Midnight Coding and Library Rain ranked #1 and #2 with scores near 9.9/10, confirming that the system handles well-represented preferences correctly. The surprise came from the sensitivity experiment: disabling mood caused Focus Flow (mood: focused) to overtake both chill songs for #1, revealing that a +2.0 binary bonus had been masking stronger numeric alignment. In the High Energy + Sad profile, Broken Compass held #1 in both runs, but Elegy in D Minor dropped out of the top 5 entirely without its mood bonus — replaced by Storm Runner, a rock/intense track with better energy fit but no emotional relevance. The nonexistent-genre profile produced identical rankings in both runs, which confirmed our expectation: when mood already contributes zero (no catalog match), disabling it changes nothing, serving as a useful control case.

See [reflection.md](reflection.md) for a per-profile comparison of the mood-enabled vs. mood-disabled outputs.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
