# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  
SongMatcher 1.0

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This recommender is for someone who just deoesn't know what to listen to, specifically for those who have multiple favorite genres with different ranges. It assumes that the user enjoys multiple types of genres. 
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Features from each song that. The user's same preferences would be considered in this ranking, the closer they are to their top preference, the higher ranking it gets. This model heavily considers the users genres and vibes as it is weighted the most. Each factor gets scored then added up, once that is done then we will find the average depending on the amount of filled preferences the user has. The more filled preferences the more accurate ranking will occur. 
---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

Theere are 20 songs in the catelog, with 17 genres and 16 moods. I did choose to add more data but I do feel like there are some musical tastes that are missing from this dataset. 

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  
I do think that my system accurately represents the users preferences when the user has their profile filled out. For example when we were given the "chill" profile, it provided us with lots of "calm" and "lofi" songs. Another aspect that I do think plays a big role in the accuracy is the different components that get considered in the ranking. My recommendr would be able to do rankings soley based off of one subtopic fo the user preferences.
---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users 

A major limitation is genre bias. Genre has the largest weight and only counts exact matches, so it acts more like a filter rather than a preference. A song in the user's genre will outrank a song from a different genre even when the other song fits the user's mood and sound much better. For example, for a pop fan whose ideal sound matches Rooftop Lights exactly, Rooftop Lights (indie pop, perfect vibe and mood) scores 5.00 and ranks below Gym Hero (pop, wrong mood, worse vibe) at 7.68, just because its genre label says "indie pop" instead of "pop." As a result, users rarely see music outside their chosen genre, even when it's a close match.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  
Profiles tested: 
1.  high-energy pop: for someone who likes upbeat pop music, high energy and enjoy dancing. 
2. chill lofi: relaxing calm music, low energy, not used for dancing 
3. deep intense rock: high energy, darker mood with wth little acoustic sound. 

What I found surprising about the results is how the recommender is able to recognize high-energy throughout the different genres. An example of this is in "high-energy" and "intense rock" where they both contained Gym is considered pop but belongs in two very different profile preferences 
---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

Additional features I would add is more songs and a way to combine the different rankings into one that better reflects the users preferences as a whole. Although I did enjoy the different rankings based solely on the user's sub-preferences I do think I could find better way to accurately recommend songs. I would want to add more songs from artists that currently have one song in my csv file so it gives more of a equal chance against the recommender. 
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

What I learned about recommender systems is that it is extremely difficult to create a "fair" recommeder system. It made me realize the importance of variety as it not only gives a fair chance for all songs to be recommended but it shows the wide range of music genres/types available. This project made me better understand recommendation systems as a whole and how my preferences and history plays a role in my algorithm. 