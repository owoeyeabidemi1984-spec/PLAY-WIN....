import time

import streamlit as st

st.set_page_config(page_title="Knowledge Quest", page_icon="🧭", layout="centered")

# --- Settings ---
TIME_LIMIT = 30 * 60  # 30 minutes in seconds
MAX_LIVES = 3
PASS_MARK = 4

st.title("🧭 Knowledge Quest")
st.caption("Save the City of Knowledge • 5 Levels • 30 Mins Mission • Age 12")

# --- Game Data ---
LEVELS = [
    {"title": "LEVEL 1 - Maths Island 🧮", "badge": "Maths Master", "qs": [
        {"q": "What is 15% of 200?", "o": ["20", "30", "25", "35"], "a": 1},
        {"q": "If 3x + 5 = 20, what is x?", "o": ["3", "5", "4", "6"], "a": 1},
        {"q": "What is 7² + 3² ?", "o": ["58", "49", "64", "52"], "a": 0},
        {"q": "A book costs ₦1,200 and is reduced by 25%. New price?", "o": ["₦900", "₦1000", "₦800", "₦950"], "a": 0},
        {"q": "What is the LCM of 6 and 8?", "o": ["12", "24", "18", "48"], "a": 1},
    ]},
    {"title": "LEVEL 2 - Word Land 📚", "badge": "Word Wizard", "qs": [
        {"q": "Choose the correct spelling:", "o": ["Necesary", "Neccessary", "Necessary", "Necessarry"], "a": 2},
        {"q": "Synonym of BRAVE is:", "o": ["Scared", "Fearless", "Weak", "Shy"], "a": 1},
        {"q": "Which is a noun?", "o": ["Quickly", "Happiness", "Run", "Beautiful"], "a": 1},
        {"q": "'He kicked the bucket' means:", "o": ["He played football", "He died", "He was angry", "He cleaned"], "a": 1},
        {"q": "Past tense of 'teach'?", "o": ["Teached", "Taught", "Teaching", "Teach"], "a": 1},
    ]},
    {"title": "LEVEL 3 - Science Lab 🔬", "badge": "Science Star", "qs": [
        {"q": "What planet is known as the Red Planet?", "o": ["Venus", "Jupiter", "Mars", "Saturn"], "a": 2},
        {"q": "What is H2O?", "o": ["Salt", "Water", "Oxygen", "Hydrogen"], "a": 1},
        {"q": "Which organ pumps blood?", "o": ["Liver", "Lung", "Heart", "Brain"], "a": 2},
        {"q": "What gas do plants absorb?", "o": ["Oxygen", "Nitrogen", "Carbon dioxide", "Helium"], "a": 2},
        {"q": "Which is a renewable energy?", "o": ["Coal", "Petrol", "Solar", "Diesel"], "a": 2},
    ]},
    {"title": "LEVEL 4 - Logic Maze 🧩", "badge": "Logic King", "qs": [
        {"q": "Next number: 2, 6, 12, 20, ?", "o": ["28", "30", "32", "26"], "a": 1},
        {"q": "If a cat has 4 legs, how many legs do 7 cats have?", "o": ["24", "28", "21", "32"], "a": 1},
        {"q": "I am odd, between 10 and 20, divisible by 3. Who am I?", "o": ["12", "15", "18", "11"], "a": 1},
        {"q": "If today is Wednesday, what day is it in 10 days?", "o": ["Friday", "Saturday", "Sunday", "Monday"], "a": 1},
        {"q": "Which does NOT belong?", "o": ["Apple", "Banana", "Carrot", "Mango"], "a": 2},
    ]},
    {"title": "LEVEL 5 - FINAL BOSS 👾", "badge": "Final Boss Slayer", "qs": [
        {"q": "What is 12 x 8 - 20 ?", "o": ["76", "96", "86", "66"], "a": 0},
        {"q": "Antonym of 'Ancient' is:", "o": ["Old", "Modern", "Past", "Rare"], "a": 1},
        {"q": "What is the chemical symbol for Gold?", "o": ["Gd", "Go", "Au", "Ag"], "a": 2},
        {"q": "If you have ₦5,000 and spend 2/5, how much is left?", "o": ["₦2,000", "₦3,000", "₦2,500", "₦3,500"], "a": 1},
        {"q": "What is 1000 + 2000 + 500 - 100?", "o": ["3,400", "3,200", "3,500", "2,900"], "a": 0},
    ]},
]

ss = st.session_state


# --- Helpers ---
def reset_game():
    for k in list(ss.keys()):
        del ss[k]
    st.rerun()


def start_level():
    """Reset per-level progress (keeps total coins/stars)."""
    ss.q = 0
    ss.correct = 0
    ss.lives = MAX_LIVES
    ss.phase = "question"  # question -> feedback -> level_end
    ss.level_start_coins = ss.coins
    ss.level_start_stars = ss.stars
    ss.last = None


def retry_level():
    """Retry the level without keeping coins/stars earned in the failed attempt."""
    ss.coins = ss.level_start_coins
    ss.stars = ss.level_start_stars
    ss.attempt += 1
    ss.q = 0
    ss.correct = 0
    ss.lives = MAX_LIVES
    ss.phase = "question"
    ss.last = None


# --- Session State ---
if "started" not in ss:
    ss.started = False
    ss.finished = False
    ss.player = "Explorer"
    ss.level = 0
    ss.coins = 0
    ss.stars = 0
    ss.badges = []
    ss.attempt = 0
    ss.start_time = None
    start_level()

# --- Start Screen ---
if not ss.started:
    name = st.text_input("Enter your name", placeholder="e.g. David")
    if st.button("▶ START MISSION", use_container_width=True):
        ss.player = name.strip() or "Explorer"
        ss.started = True
        ss.start_time = time.time()
        st.rerun()
    st.info(
        f"You need {PASS_MARK}/5 correct to pass a level. "
        f"You have {MAX_LIVES} lives per level and 30 minutes in total."
    )
    st.stop()

# --- Win Screen ---
if ss.finished:
    st.balloons()
    st.success(f"🏆 {ss.player}, You Saved The City!")
    st.write(f"Final Score: 🪙 {ss.coins} coins | ⭐ {ss.stars} stars")
    st.write("🏅 Badges: " + " • ".join(ss.badges))
    if st.button("PLAY AGAIN", use_container_width=True):
        reset_game()
    st.stop()

# --- Timer ---
remaining = int(TIME_LIMIT - (time.time() - ss.start_time))
if remaining <= 0:
    st.error(f"⏰ Time's up, {ss.player}! The mission is over.")
    st.write(f"Score: 🪙 {ss.coins} coins | ⭐ {ss.stars} stars")
    if ss.badges:
        st.write("🏅 Badges: " + " • ".join(ss.badges))
    if st.button("PLAY AGAIN", use_container_width=True):
        reset_game()
    st.stop()

# --- Level Screen ---
level_data = LEVELS[ss.level]
questions = level_data["qs"]
total_q = len(questions)

st.subheader(level_data["title"])
col1, col2, col3, col4 = st.columns(4)
col1.metric("Coins", ss.coins)
col2.metric("Stars", ss.stars)
col3.metric("Lives", "❤️" * ss.lives if ss.lives > 0 else "💔")
col4.metric("Time left", f"{remaining // 60:02d}:{remaining % 60:02d}")

if ss.phase == "question":
    st.progress(ss.q / total_q)
elif ss.phase == "feedback":
    st.progress((ss.q + 1) / total_q)
else:
    st.progress(1.0)

# ---- Phase: question ----
if ss.phase == "question":
    current = questions[ss.q]
    st.markdown(f"### Q{ss.q + 1}. {current['q']}")
    choice = st.radio(
        "Choose your answer:",
        current["o"],
        index=None,
        key=f"q_{ss.attempt}_{ss.level}_{ss.q}",
    )
    if st.button("Submit Answer ✅", use_container_width=True, disabled=choice is None):
        right_answer = current["o"][current["a"]]
        is_correct = choice == right_answer
        if is_correct:
            ss.coins += 10
            ss.stars += 1
            ss.correct += 1
        else:
            ss.lives -= 1
        ss.last = {"correct": is_correct, "answer": right_answer}
        ss.phase = "feedback"
        st.rerun()

# ---- Phase: feedback ----
elif ss.phase == "feedback":
    current = questions[ss.q]
    st.markdown(f"### Q{ss.q + 1}. {current['q']}")
    if ss.last["correct"]:
        st.success("✅ Correct! +10 coins +1 star")
    else:
        st.error(f"❌ Wrong! Correct answer was: {ss.last['answer']}")

    if st.button("Continue ▶", use_container_width=True):
        if ss.lives <= 0 or ss.q + 1 >= total_q:
            ss.phase = "level_end"
        else:
            ss.q += 1
            ss.phase = "question"
        st.rerun()

# ---- Phase: level end ----
else:
    passed = ss.lives > 0 and ss.correct >= PASS_MARK
    if passed:
        st.balloons()
        st.success(f"🎉 Level Complete! Badge Unlocked: {level_data['badge']}")
        st.write(f"Score this level: {ss.correct}/{total_q}")
        is_last = ss.level + 1 >= len(LEVELS)
        if st.button("🏁 FINISH MISSION" if is_last else "NEXT LEVEL →", use_container_width=True):
            ss.badges.append(level_data["badge"])
            if is_last:
                ss.finished = True
            else:
                ss.level += 1
                ss.attempt += 1
                start_level()
            st.rerun()
    else:
        if ss.lives <= 0:
            st.warning("💔 Game Over for this level! You ran out of lives.")
        else:
            st.error(f"You got {ss.correct}/{total_q}. You need {PASS_MARK}/{total_q} to pass.")
        if st.button("🔁 Retry Level", use_container_width=True):
            retry_level()
            st.rerun()

st.divider()
if st.button("Restart Game"):
    reset_game()
