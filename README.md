# 🎬 AI Movie Recommendation System

## Project 3 — AI Recommendation Logic

This project implements a simple recommendation system based on user preferences.
The supplied Project 3 brief asks the learner to take user interests, match preferences
using logic or similarity, and display recommended items. This implementation uses
movies as the items and genre similarity as the recommendation logic.

## Features

- Modern dark recommendation UI
- User enters interests such as `action, sci-fi`
- 40-movie local CSV dataset
- Explainable similarity calculation
- Top 5 recommendations
- Numerical similarity score between 0 and 1
- Displays matched genres for transparency
- No external API or database required

## Project Structure

```text
ai_movie_recommendation_project/
├── app.py
├── movies.csv
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.9 or newer
- Internet connection only for installing Python packages
- Streamlit

## Installation

### 1. Open the project folder

```bash
cd ai_movie_recommendation_project
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Streamlit will open the application in your browser.

## How the Recommendation Logic Works

The system follows a simple and explainable pattern-matching approach.

### Step 1 — User Input

The user enters comma-separated interests:

```text
action, sci-fi
```

### Step 2 — Convert Interests to a Set

The input is normalized and converted into tokens:

```text
{"action", "sci-fi"}
```

### Step 3 — Movie Genre Set

Each movie contains genres such as:

```text
action|sci-fi|thriller|adventure
```

which becomes:

```text
{"action", "sci-fi", "thriller", "adventure"}
```

### Step 4 — Similarity Score

The core similarity is based on set overlap:

```text
similarity = |user interests ∩ movie genres|
             --------------------------------
             |user interests ∪ movie genres|
```

This is a Jaccard-style similarity score.

A small bonus is applied for direct matched interests, and the result is capped
at `1.00`.

### Step 5 — Ranking

Every movie receives a score.

The movies are sorted from highest score to lowest score, and the top five
are displayed.

## Example

Input:

```text
action, sci-fi
```

Possible recommendations include:

```text
🎬 The Matrix
🎬 Inception
🎬 Iron Man
🎬 Avengers: Endgame
🎬 Avatar
```

The exact ranking is calculated automatically from the dataset rather than being
hard-coded.

## Why This Satisfies Project 3

The implementation directly covers the required areas:

1. **Take user input** — interests are entered through the UI.
2. **Match preferences** — user interests are compared against movie genres.
3. **Display recommended items** — the five highest-scoring movies are shown.
4. **Logic/similarity** — a transparent set-based similarity algorithm produces
   the recommendation score.

## Dataset

`movies.csv` contains two columns:

- `title` — movie title
- `genres` — pipe-separated genre labels

You can add more movies by adding rows to the CSV.

Example:

```csv
title,genres
Example Movie,action|sci-fi|thriller
```

Do not change the column names unless you also update `app.py`.

## Suggested Demo Inputs

Try these during your presentation:

```text
action, sci-fi
romance, drama
horror, thriller
animation, comedy
fantasy, adventure
```

## Presentation Explanation

A short explanation you can give:

> "This is a content-based recommendation system. The user provides interests,
> and the system compares those interests with the genres assigned to every movie.
> I use a Jaccard-style similarity score based on set intersection and union.
> Movies are then sorted according to their similarity score, and the top five
> recommendations are displayed with their scores and matched genres."

## Future Improvements

Possible extensions include:

- User ratings
- Movie descriptions
- TF-IDF and cosine similarity
- Larger datasets
- Collaborative filtering
- User profiles
- Movie posters
- Search and filtering
- Persistent recommendation history

## License

Educational project for AI recommendation-system practice.
