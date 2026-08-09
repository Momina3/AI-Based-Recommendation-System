from pathlib import Path
import re

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# DATASET
# ============================================================

DATA_FILE = Path(__file__).parent / "movies.csv"


@st.cache_data
def load_movies():
    df = pd.read_csv(DATA_FILE)
    df["genre_list"] = df["genres"].str.split("|")
    return df


movies = load_movies()


# ============================================================
# RECOMMENDATION LOGIC
# ============================================================

def normalize_text(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def calculate_similarity(user_interests, movie_genres):
    """
    Jaccard-style similarity:

        intersection / union

    A small bonus is added for direct genre matches.
    """

    user_tokens = set()

    for interest in user_interests:
        user_tokens.update(normalize_text(interest))

    movie_tokens = set(movie_genres)

    if not user_tokens or not movie_tokens:
        return 0.0, []

    matched = sorted(user_tokens & movie_tokens)

    union = user_tokens | movie_tokens

    score = len(matched) / len(union)

    # Direct-match bonus
    score += 0.05 * len(matched)

    return min(score, 1.0), matched


def recommend(user_input, top_n=5):

    interests = [
        item.strip().lower()
        for item in user_input.split(",")
        if item.strip()
    ]

    if not interests:
        return pd.DataFrame()

    recommendations = []

    for _, movie in movies.iterrows():

        score, matched = calculate_similarity(
            interests,
            movie["genre_list"]
        )

        recommendations.append({
            "title": movie["title"],
            "genres": movie["genres"].replace("|", " • "),
            "score": score,
            "matched": matched,
        })

    result = pd.DataFrame(recommendations)

    result = result[result["score"] > 0]

    result = result.sort_values(
        by=["score", "title"],
        ascending=[False, True]
    )

    return result.head(top_n).reset_index(drop=True)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   APPLICATION
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 8% 8%,
            rgba(80, 65, 180, 0.20),
            transparent 32%
        ),
        radial-gradient(
            circle at 92% 12%,
            rgba(0, 170, 200, 0.10),
            transparent 30%
        ),
        #070a12;

    color: #f5f7ff;
}


.block-container {
    max-width: 1050px;
    padding-top: 2.4rem;
    padding-bottom: 3rem;
}


/* ============================================================
   HEADER
   ============================================================ */

.hero-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: #f7f8ff;
}

.hero-subtitle {
    text-align: center;
    color: #9da8bf;
    font-size: 1rem;
    margin-top: 8px;
    margin-bottom: 32px;
}


/* ============================================================
   NATIVE STREAMLIT CONTAINERS
   ============================================================ */

/*
   Important:
   We DO NOT style arbitrary HTML wrapper divs here.
   The panels are created using st.container(border=True).
*/

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 20, 32, 0.82);
    border: 1px solid #273149 !important;
    border-radius: 16px !important;
}


/* ============================================================
   SECTION TITLES
   ============================================================ */

.section-title {
    font-size: 1.05rem;
    font-weight: 750;
    color: #f5f7ff;
    margin-bottom: 10px;
}


/* ============================================================
   INPUT
   ============================================================ */

div[data-testid="stTextInput"] {
    margin-top: 0 !important;
}

div[data-testid="stTextInput"] label {
    display: none !important;
}

div[data-testid="stTextInput"] input {
    background: #111725 !important;
    color: #f5f7ff !important;

    border: 1px solid #29334b !important;
    border-radius: 10px !important;

    height: 46px !important;

    padding: 0 14px !important;

    font-size: 0.94rem !important;

    box-shadow: none !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #6978ff !important;
    box-shadow: 0 0 0 1px #6978ff !important;
}


/* ============================================================
   HELPER TEXT
   ============================================================ */

.helper-text {
    color: #7f899f;
    font-size: 0.76rem;
    margin-top: 7px;
    margin-bottom: 15px;
}


/* ============================================================
   BUTTONS
   ============================================================ */

div[data-testid="stButton"] button {
    width: 100%;
    height: 44px;

    border-radius: 10px;

    font-weight: 700;
    font-size: 0.88rem;

    border: none;
}


/* ============================================================
   HOW IT WORKS
   ============================================================ */

.info-box {
    background: #111725;
    border: 1px solid #252e43;
    border-radius: 14px;

    padding: 19px;

    margin-top: 18px;
}

.info-title {
    color: #f5f7ff;

    font-size: 1rem;
    font-weight: 750;

    margin-bottom: 9px;
}

.info-text {
    color: #9da7bd;

    font-size: 0.82rem;

    line-height: 1.65;
}


/* ============================================================
   RECOMMENDATION CARD
   ============================================================ */

.movie-card {
    background: #121827;

    border: 1px solid #252e43;
    border-radius: 14px;

    padding: 15px 17px;

    margin-bottom: 11px;
}

.movie-title {
    color: #f7f8ff;

    font-size: 0.97rem;
    font-weight: 750;
}

.movie-genres {
    color: #8290b0;

    font-size: 0.76rem;

    margin-top: 6px;
}

.movie-match {
    color: #91a1c5;

    font-size: 0.76rem;

    margin-top: 6px;
}

.movie-score {
    text-align: right;

    min-width: 70px;
}

.score-number {
    color: #f5f7ff;

    font-size: 1rem;
    font-weight: 800;
}

.score-label {
    color: #7f8ba5;

    font-size: 0.62rem;

    text-transform: uppercase;

    letter-spacing: 0.05em;

    margin-top: 3px;
}


/* ============================================================
   EMPTY STATE
   ============================================================ */

.empty-state {
    text-align: center;

    color: #858fa7;

    padding: 45px 15px;

    font-size: 0.86rem;
}

.empty-icon {
    font-size: 2rem;

    margin-bottom: 9px;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;

    color: #59647b;

    font-size: 0.7rem;

    margin-top: 25px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="hero-title">🎬 AI Movie Recommendation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Discover movies by matching your interests with movie genres.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# MAIN LAYOUT
# ============================================================

left_col, right_col = st.columns(
    [1, 1.35],
    gap="large"
)


# ============================================================
# LEFT COLUMN
# ============================================================

with left_col:

    # --------------------------------------------------------
    # INTERESTS PANEL
    # --------------------------------------------------------

    with st.container(border=True):

        st.markdown(
            '<div class="section-title">Your Interests</div>',
            unsafe_allow_html=True
        )

        interests = st.text_input(
            "Movie interests",
            value=st.session_state.get(
                "interests",
                "action, sci-fi"
            ),
            placeholder="e.g. action, sci-fi, thriller",
            label_visibility="collapsed"
        )

        st.markdown(
            '<div class="helper-text">'
            'Separate interests with commas.'
            '</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(
            [1.2, 0.8],
            gap="small"
        )

        with col1:

            recommend_clicked = st.button(
                "✨ Recommend",
                type="primary",
                use_container_width=True
            )

        with col2:

            reset_clicked = st.button(
                "↻ Reset",
                use_container_width=True
            )


    # --------------------------------------------------------
    # BUTTON ACTIONS
    # --------------------------------------------------------

    if recommend_clicked:

        st.session_state["interests"] = interests

        st.rerun()


    if reset_clicked:

        st.session_state["interests"] = ""

        st.rerun()


    # --------------------------------------------------------
    # HOW IT WORKS
    # --------------------------------------------------------

    st.markdown(
        '<div class="info-box">'
        '<div class="info-title">How it works</div>'
        '<div class="info-text">'
        'The system converts your interests and each movie\'s '
        'genres into sets, calculates their similarity, and '
        'ranks movies from the highest score to the lowest.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# RIGHT COLUMN
# ============================================================

with right_col:

    # --------------------------------------------------------
    # RECOMMENDATIONS PANEL
    # --------------------------------------------------------

    with st.container(border=True):

        st.markdown(
            '<div class="section-title">Recommendations</div>',
            unsafe_allow_html=True
        )

        current_interests = st.session_state.get(
            "interests",
            interests
        )

        # ----------------------------------------------------
        # EMPTY INPUT
        # ----------------------------------------------------

        if not current_interests.strip():

            st.markdown(
                '<div class="empty-state">'
                '<div class="empty-icon">🎯</div>'
                'Enter your interests and click '
                '<b>Recommend</b>.'
                '</div>',
                unsafe_allow_html=True
            )

        else:

            results = recommend(
                current_interests,
                top_n=5
            )

            # ------------------------------------------------
            # NO MATCHES
            # ------------------------------------------------

            if results.empty:

                st.markdown(
                    '<div class="empty-state">'
                    '<div class="empty-icon">🔎</div>'
                    'No matching movies found.<br>'
                    'Try interests such as '
                    '<b>action, sci-fi</b>.'
                    '</div>',
                    unsafe_allow_html=True
                )

            # ------------------------------------------------
            # DISPLAY MOVIES
            # ------------------------------------------------

            else:

                for _, movie in results.iterrows():

                    score = movie["score"]

                    percentage = round(score * 100)

                    matched = (
                        ", ".join(movie["matched"])
                        if movie["matched"]
                        else "general match"
                    )

                    # This is ONE complete HTML block.
                    # It is NOT opened in one markdown call
                    # and closed in another.

                    card = f"""
<div class="movie-card">
<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:20px;">
<div style="flex:1;">
<div class="movie-title">🎬 {movie["title"]}</div>
<div class="movie-genres">{movie["genres"]}</div>
<div class="movie-match">Matched: {matched}</div>
</div>
<div class="movie-score">
<div class="score-number">{score:.2f}</div>
<div class="score-label">{percentage}% match</div>
</div>
</div>
</div>
"""

                    st.markdown(
                        card,
                        unsafe_allow_html=True
                    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    f'Dataset: {len(movies)} movies'
    '&nbsp;&nbsp;•&nbsp;&nbsp;'
    'Recommendation method: similarity-based genre matching'
    '</div>',
    unsafe_allow_html=True
)