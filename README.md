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

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.
logic: 
- input: User will have the ability to input their top two favorite genres and moods. 
-scoring: 4.0(genre)+2.5(vibe)+2.0(artist)+1.5(mood)
each subcategory would get a scoring of 0-10 depending on how close it is from the target. 
- ranking: Ranking is based on the highest score out of each scored song.

In this recommendation system, the song features that will be apart of the recommending process include genre, energy, valence, dancabiltiy, acousticness, artist, and mood. I decided to have genre to take highest priority in this case since artists could have multiple genres and the user may have a wide range in music taeste. the "User profile" will contain favorite_genres  (top 2), favorite_mood, target_energy, target_valence, target_danceability, and target_acrouticness. The recommender will score a song based on how well it fits the users preferences. Based on how close category is to the user's preference it will get scored 0-10. Each category gets weighted, with genre at 4.0, vibe 2.5, artist 2.0 and mood at 1.5  

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

Output from `python -m src.main` for the default pop/happy user, using the `balanced` strategy (genre 4.0, vibe 2.5, artist 2.0, mood 1.5). No favorite artist was given, so artist is left out of the score.

```

================================================================
 BALANCED STRATEGY
 Genre leads, with vibe, artist, and mood as supporting signals.
================================================================

 #1  Sunrise City                              9.93 / 10
     Neon Echo · pop · happy
     ████████████████████
       ✓ matches your top genre (pop)
       ✓ closely matches the vibe you like
       ✓ has your top mood (happy)

 #2  Gym Hero                                  7.82 / 10
     Max Pulse · pop · intense
     ████████████████░░░░
       ✓ matches your top genre (pop)
       ✓ closely matches the vibe you like

 #3  Rooftop Lights                            4.83 / 10
     Indigo Parade · indie pop · happy
     ██████████░░░░░░░░░░
       ✓ closely matches the vibe you like
       ✓ has your top mood (happy)

 #4  Calle Dorada                              2.88 / 10
     Los Faroles · latin · energetic
     ██████░░░░░░░░░░░░░░
       ✓ closely matches the vibe you like

 #5  Afterglow Rush                            2.80 / 10
     Neon Echo · edm · euphoric
     ██████░░░░░░░░░░░░░░
       ✓ closely matches the vibe you like

----------------------------------------------------------------

================================================================
 MOOD FIRST STRATEGY
 Matches how the user wants to feel, regardless of genre.
================================================================

 #1  Sunrise City                              9.93 / 10
     Neon Echo · pop · happy
     ████████████████████
       ✓ matches your top genre (pop)
       ✓ closely matches the vibe you like
       ✓ has your top mood (happy)

 #2  Rooftop Lights                            8.15 / 10
     Indigo Parade · indie pop · happy
     ████████████████░░░░
       ✓ closely matches the vibe you like
       ✓ has your top mood (happy)

 #3  Gym Hero                                  4.68 / 10
     Max Pulse · pop · intense
     █████████░░░░░░░░░░░
       ✓ matches your top genre (pop)
       ✓ closely matches the vibe you like

 #4  Calle Dorada                              3.07 / 10
     Los Faroles · latin · energetic
     ██████░░░░░░░░░░░░░░
       ✓ closely matches the vibe you like

 #5  Afterglow Rush                            2.99 / 10
     Neon Echo · edm · euphoric
     ██████░░░░░░░░░░░░░░
       ✓ closely matches the vibe you like

----------------------------------------------------------------

================================================================
 VIBE FIRST STRATEGY
 Matches the sound (energy, valence, danceability, acousticness).
================================================================

 #1  Sunrise City                              9.88 / 10
     Neon Echo · pop · happy
     ████████████████████
       ✓ matches your top genre (pop)
       ✓ closely matches the vibe you like
       ✓ has your top mood (happy)

 #2  Rooftop Lights                            8.03 / 10
     Indigo Parade · indie pop · happy
     ████████████████░░░░
       ✓ closely matches the vibe you like
       ✓ has your top mood (happy)

 #3  Gym Hero                                  6.68 / 10
     Max Pulse · pop · intense
     █████████████░░░░░░░
       ✓ matches your top genre (pop)
       ✓ closely matches the vibe you like

 #4  Calle Dorada                              5.12 / 10
     Los Faroles · latin · energetic
     ██████████░░░░░░░░░░
       ✓ closely matches the vibe you like

 #5  Afterglow Rush                            4.99 / 10
     Neon Echo · edm · euphoric
     ██████████░░░░░░░░░░
       ✓ closely matches the vibe you like

----------------------------------------------------------------

================================================================
 DISCOVERY STRATEGY
 Ignores favorite artists and leans on vibe to surface new music.
================================================================

 #1  Sunrise City                              9.89 / 10
     Neon Echo · pop · happy
     ████████████████████
       ✓ matches your top genre (pop)
       ✓ closely matches the vibe you like
       ✓ has your top mood (happy)

 #2  Rooftop Lights                            8.48 / 10
     Indigo Parade · indie pop · happy
     █████████████████░░░
       ✓ closely matches the vibe you like
       ✓ has your top mood (happy)

 #3  Gym Hero                                  5.76 / 10
     Max Pulse · pop · intense
     ████████████░░░░░░░░
       ✓ matches your top genre (pop)
       ✓ closely matches the vibe you like

 #4  Calle Dorada                              4.61 / 10
     Los Faroles · latin · energetic
     █████████░░░░░░░░░░░
       ✓ closely matches the vibe you like

 #5  Afterglow Rush                            4.49 / 10
     Neon Echo · edm · euphoric
     █████████░░░░░░░░░░░
       ✓ closely matches the vibe you like

----------------------------------------------------------------

=== Strategy comparison ===

Rank  balanced               mood_first             vibe_first             discovery             
--------------------------------------------------------------------------------------------------
#1    Sunrise City           Sunrise City           Sunrise City           Sunrise City          
#2    Gym Hero               Rooftop Lights         Rooftop Lights         Rooftop Lights        
#3    Rooftop Lights         Gym Hero               Gym Hero               Gym Hero              
#4    Calle Dorada           Calle Dorada           Calle Dorada           Calle Dorada          
#5    Afterglow Rush         Afterglow Rush         Afterglow Rush         Afterglow Rush   

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



