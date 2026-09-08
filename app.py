"""
CPA Math 6 — Day 6: Area Unlocks the Missing Side
Built to match the visual/interactive structure of the Day 5 app
("Area Is Multiplication") by Xavier Honablue, M.Ed — Chandler Park Academy.

Run locally with:  streamlit run streamlit_app.py
Deploy the same way Day 5 was deployed (push this folder to the GitHub repo
connected to your Streamlit Community Cloud app, or create a new app there).
"""

import json
import os
import random
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

# ----------------------------------------------------------------------
# Page config & theme
# ----------------------------------------------------------------------
st.set_page_config(page_title="Day 6 — Area Unlocks the Missing Side", page_icon="📐", layout="wide")

NAVY = "#1b3a5c"
NAVY_LIGHT = "#eef4fa"
NAVY_BORDER = "#2c4a6e"
GREEN = "#3f7d55"
GREEN_LIGHT = "#eef7f0"
GOLD = "#8a5a20"
GOLD_LIGHT = "#f6ecd9"
RED = "#b03a2e"
RED_LIGHT = "#fdf1ef"

CUSTOM_CSS = f"""
<style>
.box {{
    border: 2px solid {NAVY};
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
    background: white;
}}
.pill {{
    display: inline-block;
    color: white;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.4px;
    padding: 4px 12px;
    border-radius: 12px;
    margin-bottom: 8px;
}}
.box-readaloud {{ border-color: {NAVY}; }}
.box-readaloud .pill {{ background: {NAVY}; }}
.box-readaloud p {{ font-style: italic; margin: 4px 0 0 0; }}

.box-literacy {{ border-color: {NAVY_BORDER}; background: {NAVY_LIGHT}; }}
.box-literacy .pill {{ background: {NAVY_BORDER}; }}

.box-existing {{ border-color: {GREEN}; background: {GREEN_LIGHT}; }}
.box-existing .pill {{ background: {GREEN}; }}

.box-tools {{ border-color: {GOLD}; background: {GOLD_LIGHT}; }}
.box-tools .pill {{ background: {GOLD}; }}

.box-observer {{ border: 2px dashed {RED}; background: {RED_LIGHT}; }}
.box-observer .pill {{ background: {RED}; }}

.ask {{ color: {RED}; font-weight: 700; margin-top: 8px; }}

.roadmap-title {{ color: {NAVY}; font-weight: 700; font-size: 15px; margin-bottom: 0; }}
.roadmap-sub {{ color: #5a6672; font-size: 11.5px; margin-top: -4px; }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def box(kind, pill, body_html):
    st.markdown(
        f'<div class="box box-{kind}"><span class="pill">{pill}</span>{body_html}</div>',
        unsafe_allow_html=True,
    )


def read_aloud(text):
    box("readaloud", "🔊 READ ALOUD", f"<p>&ldquo;{text}&rdquo;</p>")


def ask_the_class(text):
    st.markdown(f'<p class="ask">❓ Ask the class: {text}</p>', unsafe_allow_html=True)


# ----------------------------------------------------------------------
# Observer notes — a running teacher log, persisted to a local JSON file
# ----------------------------------------------------------------------
NOTES_FILE = os.path.join(os.path.dirname(__file__), "observer_notes.json")
DEFAULT_NOTES = [
    {
        "date": "Day 5",
        "note": "Several students labeled every four-sided figure a “square,” including "
                "rectangles that were clearly longer than they were wide. Left unaddressed, this "
                "will undermine Day 6's work on base vs. height as two different measurements. "
                "Day 6 opens with a direct square-vs-rectangle re-teach before any area work begins.",
    }
]


def load_notes():
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE) as f:
                return json.load(f)
        except Exception:
            return list(DEFAULT_NOTES)
    return list(DEFAULT_NOTES)


def save_notes(notes):
    try:
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=2)
    except Exception:
        pass  # read-only filesystem (e.g. some cloud hosts) — notes still live for this session


if "observer_notes" not in st.session_state:
    st.session_state.observer_notes = load_notes()

# ----------------------------------------------------------------------
# Sidebar — Sign In + Roadmap (mirrors the Day 5 app)
# ----------------------------------------------------------------------
with st.sidebar:
    st.subheader("Sign In")
    st.text_input("Your name:", key="student_name")
    st.selectbox("Choose your shape avatar:", ["Rectangle", "Square", "Triangle", "Circle", "Hexagon"], key="avatar")
    st.selectbox(
        "Pick your learning mode:",
        ["Focus Champ", "Growth Mode", "Problem Solver", "Data Boss", "Brain Builder"],
        key="learning_mode",
    )
    st.markdown("---")
    st.markdown('<p class="roadmap-title">Day 6 Roadmap</p>', unsafe_allow_html=True)
    st.markdown('<p class="roadmap-sub">55-minute period — Area Unlocks the Missing Side</p>', unsafe_allow_html=True)

    steps = [
        "1. Welcome Back",
        "2. Recitation: Groups, Bags & Tiles",
        "3. Square vs. Rectangle",
        "4. Area of the Floor",
        "5. Find the Missing Side",
        "6. Discuss It & Connect It",
        "7. Project: Tile the Floor Competition",
        "8. Engage / Explore / Enrich",
    ]
    if "step" not in st.session_state:
        st.session_state.step = 0
    for i, label in enumerate(steps):
        marker = "▶ " if i == st.session_state.step else ""
        if st.button(marker + label, key=f"nav_{i}", use_container_width=True):
            st.session_state.step = i
            st.rerun()

# ----------------------------------------------------------------------
# Drawing helpers (matplotlib, styled to match the PDF diagrams)
# ----------------------------------------------------------------------
def draw_grid(base, height, area_label=None, fill="#dbe8f6", edge=NAVY, figsize=(4.4, 3.2)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.add_patch(patches.Rectangle((0, 0), base, height, facecolor=fill, edgecolor=edge, linewidth=2.2))
    for c in range(base + 1):
        ax.plot([c, c], [0, height], color="#9db6cc", linewidth=0.6)
    for r in range(height + 1):
        ax.plot([0, base], [r, r], color="#9db6cc", linewidth=0.6)
    if area_label:
        ax.text(base / 2, height / 2, area_label, ha="center", va="center",
                 fontsize=13, fontweight="bold", color=NAVY)
    ax.set_xlim(-0.6, base + 0.6)
    ax.set_ylim(-0.6, height + 0.6)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def draw_composite(a_base, a_height, top_width, b_height):
    """L shape: top piece (top_width x b_height) + bottom piece (full a_base x a_height)."""
    fig, ax = plt.subplots(figsize=(5, 4))
    # bottom rectangle
    ax.add_patch(patches.Rectangle((0, 0), a_base, a_height, facecolor="#dbe8f6", edgecolor=NAVY, linewidth=2.2))
    # top rectangle
    ax.add_patch(patches.Rectangle((0, a_height), top_width, b_height, facecolor="#dbe8f6", edgecolor=NAVY, linewidth=2.2))
    # dashed split line
    ax.plot([0, top_width], [a_height, a_height], linestyle="--", color=GOLD, linewidth=1.6)
    ax.text(top_width / 2, a_height + b_height / 2, "A", ha="center", va="center", fontsize=13, fontweight="bold", color=NAVY)
    ax.text(a_base / 2, a_height / 2, "B", ha="center", va="center", fontsize=13, fontweight="bold", color=NAVY)
    ax.set_xlim(-1.2, a_base + 1.2)
    ax.set_ylim(-1.2, a_height + b_height + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


# ----------------------------------------------------------------------
# Roadmap step content
# ----------------------------------------------------------------------
step = st.session_state.step
name = st.session_state.get("student_name", "") or "class"

st.markdown(f"## {steps[step]}")
st.progress((step + 1) / len(steps))

if step == 0:
    box(
        "observer",
        "🔎 OBSERVER NOTE — carried from Day 5",
        f"<p style='margin:0'>{st.session_state.observer_notes[0]['note']}</p>",
    )
    read_aloud(
        "Yesterday we proved that area is multiplication — rows times columns, base times height. "
        "Today we run that idea two new ways. First, some of you were still mixing up squares and "
        "rectangles, so we are going to nail that down for good. Then I'm going to give you the AREA "
        "of a shape and only ONE side — and you are going to work backward to find the missing side. "
        "By the end of class you'll also be able to find the area of a floor that isn't just one "
        "plain rectangle."
    )
    box("tools", "Today's tools",
        "Graph paper and colored pencils &middot; floor tiles or a taped grid on the classroom floor "
        "&middot; journal &middot; exit ticket.")

elif step == 1:
    st.write("**Purpose:** Students stand and orally rehearse group-structure language, then flip it "
             "into division — the exact move today's new skill depends on.")
    box("tools", "How to run it",
        "Students stand in rows. Read one prompt card at a time. The row (or a called-on student) "
        "stands taller, states the sentence frame out loud, and the whole class chorally finishes "
        "the sentence. Rotate so every row gets at least one &ldquo;groups&rdquo; card and one "
        "&ldquo;missing side&rdquo; card.")

    cards = [
        ("5 bags, 4 apples in each bag",
         "5 groups of 4. That's 5 bags, each with 4 apples. 4+4+4+4+4 = 20. So 5 × 4 = 20 apples."),
        ("6 rows of tiles, 3 tiles in each row",
         "6 groups of 3. That's 6 rows, 3 tiles in each row. 3+3+3+3+3+3 = 18. So 6 × 3 = 18 tiles — "
         "18 square units of area."),
        ("7 bags, 5 apples in each bag",
         "7 groups of 5. 5+5+5+5+5+5+5 = 35. So 7 × 5 = 35 apples."),
        ("4 rows of tiles, 9 tiles in each row",
         "4 groups of 9. So 4 × 9 = 36 tiles — 36 square units."),
        ("(reverse!) 24 apples, packed evenly into 6 bags",
         "24 apples in 6 equal groups. 24 ÷ 6 = 4. So each bag has 4 apples."),
        ("(reverse!) a floor covered by 30 square tiles, laid out in 6 rows",
         "30 tiles in 6 equal rows. 30 ÷ 6 = 5. So each row has 5 tiles — that's the missing side."),
    ]
    if "recite_idx" not in st.session_state:
        st.session_state.recite_idx = 0
    idx = st.session_state.recite_idx
    prompt, answer = cards[idx]
    st.markdown(f"#### Card {idx + 1} of {len(cards)}")
    st.info(f"**Teacher reads:** {prompt}")
    if st.button("🔊 Reveal the class recitation"):
        st.success(answer)
    c1, c2 = st.columns(2)
    if c1.button("⬅ Previous card") and idx > 0:
        st.session_state.recite_idx -= 1
        st.rerun()
    if c2.button("Next card ➡") and idx < len(cards) - 1:
        st.session_state.recite_idx += 1
        st.rerun()
    ask_the_class("In the last card, which number was the AREA, which was the already-known side, "
                  "and which number did we just find? What operation undid the multiplication?")

elif step == 2:
    box("literacy", "MATH LITERACY: UNLOCK THE WORDS",
        "A <b>rectangle</b> is a 4-sided shape with four right (90°) angles, where opposite sides are "
        "equal in length. A <b>square</b> is a special rectangle where <b>all four</b> sides are equal "
        "in length — not just opposite sides. Every square passes the rectangle test, so every square "
        "<b>is</b> a rectangle — but not every rectangle is a square.")

    col1, col2 = st.columns(2)
    with col1:
        w = st.slider("Width (in)", 2, 10, 4, key="sq_w")
    with col2:
        h = st.slider("Height (in)", 2, 10, 4, key="sq_h")
    fig = draw_grid(w, h, fill="#dbe8f6")
    st.pyplot(fig, use_container_width=False)
    if w == h:
        st.success(f"All four sides are {w} in — this is a **SQUARE** (and also a rectangle!).")
    else:
        st.info(f"Sides are {w} in and {h} in — opposite sides match, but not all four, so this is a "
                f"**RECTANGLE** (not a square).")

    box("existing", "DEMONSTRATION",
        "Hold up (or draw on graph paper) a 4 in × 4 in square and a 4 in × 8 in rectangle. Have "
        "students measure or count grid squares along <b>each</b> of the four sides out loud.")
    ask_the_class("Could a rectangle with sides 6 in and 6 in ever NOT be a square? Why did some of "
                  "you call yesterday's 8×3 rectangle a &ldquo;square&rdquo; — what caused that mix-up?")

elif step == 3:
    read_aloud(
        "Let's go back to something real: this floor. If our tile grid is 9 tiles across and 5 tiles "
        "deep, how many square tiles cover the whole floor? Don't multiply yet — count with me first."
    )
    col1, col2 = st.columns(2)
    with col1:
        base = st.slider("Base (tiles across)", 3, 14, 9, key="floor_base")
    with col2:
        height = st.slider("Height (tiles deep)", 3, 10, 5, key="floor_height")
    fig = draw_grid(base, height)
    st.pyplot(fig, use_container_width=False)
    st.markdown(f"**Area = {base} × {height} = {base * height} square tiles**")

    st.markdown("##### Now flip it")
    st.write("Suppose I only tell you the total tiles and one side — how many tiles across is it?")
    area_given = base * height
    st.write(f"Floor covers **{area_given} square tiles** and is **{height} tiles deep**.")
    guess = st.number_input("How many tiles across? (Area ÷ height)", min_value=0, step=1, key="floor_guess")
    if st.button("Check", key="check_floor"):
        if guess == base:
            st.success(f"Yes! {area_given} ÷ {height} = {base} tiles across.")
        else:
            st.error(f"Not quite. {area_given} ÷ {height} = {base} tiles across. Try the division again.")

elif step == 4:
    st.markdown(
        f'<div class="box box-literacy"><span class="pill">MATH LITERACY: UNLOCK THE WORDS</span>'
        f'Division is the <b>inverse</b> (undoing) operation of multiplication. If Area = base × height, '
        f'then dividing the Area by one known side always leaves the other side.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='text-align:center;font-size:20px;font-weight:700;color:%s;margin:14px 0;'>"
        "Area = base × height &nbsp;—&nbsp; base = Area ÷ height &nbsp;—&nbsp; height = Area ÷ base</div>"
        % NAVY, unsafe_allow_html=True,
    )

    if "missing_problem" not in st.session_state:
        st.session_state.missing_problem = None

    def new_problem():
        b = random.randint(3, 12)
        h = random.randint(3, 12)
        area = b * h
        hide_base = random.choice([True, False])
        st.session_state.missing_problem = {"b": b, "h": h, "area": area, "hide_base": hide_base}

    if st.session_state.missing_problem is None:
        new_problem()
    p = st.session_state.missing_problem

    if p["hide_base"]:
        st.write(f"A rectangle has an **area of {p['area']} sq ft** and a **height of {p['h']} ft**. "
                 f"Find the base.")
        answer = p["b"]
        known = p["h"]
    else:
        st.write(f"A rectangle has an **area of {p['area']} sq ft** and a **base of {p['b']} ft**. "
                 f"Find the height.")
        answer = p["h"]
        known = p["b"]

    guess = st.number_input("Missing side (ft):", min_value=0, step=1, key=f"missing_guess_{id(p)}")
    c1, c2 = st.columns(2)
    if c1.button("Check answer"):
        if guess == answer:
            st.success(f"Correct! {p['area']} ÷ {known} = {answer} ft.")
        else:
            st.error(f"Not yet. {p['area']} ÷ {known} = {answer} ft. Try again.")
    if c2.button("New problem"):
        new_problem()
        st.rerun()

    st.markdown("##### Worked examples")
    st.write("**Example 1:** Area = 48 sq ft, base = 8 ft → height = 48 ÷ 8 = **6 ft**.")
    st.write("**Example 2:** Area = 63 sq in, height = 7 in → base = 63 ÷ 7 = **9 in**.")
    st.write("**Example 3 (floor-themed):** A reading rug covers 36 square tiles and is 6 tiles wide. "
             "36 ÷ 6 = **6 tiles long**. *(Ask: is this rug a square or a rectangle?)*")
    ask_the_class("If I gave you the area and BOTH sides were unknown, could you solve it with just "
                  "division? What else would you need to know?")

elif step == 5:
    read_aloud(
        "Real floors aren't always one neat rectangle — think of a hallway that opens into a closet, "
        "or an L-shaped reading corner. We split the shape into two rectangles we already know how to "
        "handle, find each area, then add."
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        a_base = st.slider("Bottom piece width (ft)", 6, 16, 12, key="c_abase")
        a_height = st.slider("Bottom piece height (ft)", 2, 8, 5, key="c_aheight")
    with col2:
        top_width = st.slider("Top piece width (ft)", 2, a_base - 1, min(7, a_base - 1), key="c_topw")
        b_height = st.slider("Top piece height (ft)", 1, 6, 4, key="c_bheight")
    fig = draw_composite(a_base, a_height, top_width, b_height)
    with col3:
        st.pyplot(fig, use_container_width=False)

    area_a = top_width * b_height
    area_b = a_base * a_height
    total = area_a + area_b
    st.markdown(f"**Area A** = {top_width} × {b_height} = {area_a} sq ft")
    st.markdown(f"**Area B** = {a_base} × {a_height} = {area_b} sq ft")
    st.markdown(f"### Total area = {area_a} + {area_b} = **{total} sq ft**")
    ask_the_class("Where did we draw the dashed split line? Could we split this shape a different way "
                  "and still get the same total?")

elif step == 6:
    read_aloud(
        "Here's today's challenge: each team is going to tile a real floor with real tiles — and the "
        "winning team is the one who can PROVE their area is correct, not just guess it. To prove it, "
        "you have to show me two things clearly: how many groups of rows you laid down, and exactly "
        "how many tiles are in ONE of those rows. If both of those are accurate, your area will be "
        "accurate."
    )
    box("tools", "The rules",
        "1) Lay tiles edge-to-edge, no gaps, no overlaps, until the outline is covered. "
        "2) <b>Demonstrate the number of groups</b>: count each row out loud — \"1 group, 2 groups...\" "
        "3) <b>Demonstrate the size of one group</b>: count the tiles in one row out loud. "
        "4) Multiply: groups × size of one group = area, in square tiles. "
        "5) Say the full sentence: \"We have ___ groups of ___, so the area is ___ square tiles.\"")

    with st.expander("👩‍🏫 Teacher: set the official floor (kept hidden from students until you reveal it)"):
        c1, c2 = st.columns(2)
        with c1:
            official_rows = st.number_input("Official number of groups (rows)", min_value=2, max_value=20, value=6, key="official_rows")
        with c2:
            official_size = st.number_input("Official size of one group (tiles per row)", min_value=2, max_value=20, value=7, key="official_size")
        reveal = st.checkbox("Reveal the official floor to the class", key="reveal_floor")
        if reveal:
            fig = draw_grid(official_size, official_rows, area_label=f"{official_rows*official_size} sq tiles")
            st.pyplot(fig, use_container_width=False)
            st.markdown(f"**Official area = {official_rows} groups × {official_size} = {official_rows*official_size} square tiles**")

    st.markdown("##### 🏆 Team submissions & leaderboard")
    if "team_submissions" not in st.session_state:
        st.session_state.team_submissions = []

    with st.form("team_submit_form", clear_on_submit=True):
        tc1, tc2, tc3 = st.columns(3)
        team_name = tc1.text_input("Team name")
        groups_claimed = tc2.number_input("Number of groups (rows) counted", min_value=0, step=1)
        size_claimed = tc3.number_input("Size of one group (tiles) counted", min_value=0, step=1)
        submitted = st.form_submit_button("Submit team result")
        if submitted:
            if team_name.strip():
                area_claimed = groups_claimed * size_claimed
                official_area = st.session_state.get("official_rows", 6) * st.session_state.get("official_size", 7)
                correct = (
                    groups_claimed == st.session_state.get("official_rows", 6)
                    and size_claimed == st.session_state.get("official_size", 7)
                )
                st.session_state.team_submissions.append({
                    "team": team_name.strip(),
                    "groups": groups_claimed,
                    "size": size_claimed,
                    "area": area_claimed,
                    "correct": correct,
                    "time": datetime.now().strftime("%H:%M:%S"),
                })
            else:
                st.warning("Enter a team name before submitting.")

    if st.session_state.team_submissions:
        rows = sorted(st.session_state.team_submissions, key=lambda r: (not r["correct"], r["time"]))
        st.table([
            {
                "Team": r["team"],
                "Groups": r["groups"],
                "Size of 1 group": r["size"],
                "Area (sq tiles)": r["area"],
                "Result": "✅ Correct" if r["correct"] else "❌ Try again",
                "Submitted": r["time"],
            }
            for r in rows
        ])
        winners = [r["team"] for r in rows if r["correct"]]
        if winners:
            st.success(f"🏆 First accurate team: **{winners[0]}**")
    else:
        st.caption("No team results submitted yet.")

    ask_the_class("Why does it matter that every row has the same number of tiles? What would happen "
                  "to our multiplication shortcut if one row had extra tiles crammed in?")

elif step == 7:
    st.markdown("#### Engage / Explore / Enrich stations")
    tabs = st.tabs(["Engage (all)", "Explore (on-level)", "Enrich (extend)"])
    with tabs[0]:
        st.write("Independent practice: **Day 6 Worksheet** and **Day 6 ELA-Math Language Sheet** — "
                 "square vs. rectangle ID, given-area problems, composite-rectangle floor plans, and "
                 "the tiling-competition vocabulary and writing prompts.")
    with tabs[1]:
        st.write("Partner check: swap worksheets and re-do each other's division for Part 3, then "
                 "compare.")
    with tabs[2]:
        st.write("A classroom's reading corner is L-shaped. The whole rectangle it sits inside would "
                 "be 10 ft by 8 ft, but a 4 ft by 3 ft closet is cut out of one corner. What is the "
                 "area of the reading corner? *(Hint: find the big rectangle's area, then subtract "
                 "the closet.)*")

    box("existing", "EXIT TICKET",
        "Using your OWN team's competition floor: state the number of groups (rows), the size of one "
        "group (tiles per row), and the total area in tile units. Then: a rectangle has an area of "
        "54 sq cm and a height of 6 cm — find the base, and state whether it could also be a square.")

    st.markdown("---")
    st.markdown("#### 🔎 Observer Notes (running log)")
    st.caption("A running teacher log carried day to day. Today's entry is pre-loaded below — add "
               "what you noticed in class today, then Save.")
    for n in st.session_state.observer_notes:
        st.markdown(f"**{n['date']}:** {n['note']}")
    new_note = st.text_area("Add a new observation:", key="new_observer_note",
                             placeholder="e.g. Most students found the missing side confidently, but "
                                         "a few still divided the wrong number by the wrong side.")
    if st.button("Save observation"):
        if new_note.strip():
            st.session_state.observer_notes.append(
                {"date": f"Day 6 — {datetime.now().strftime('%Y-%m-%d')}", "note": new_note.strip()}
            )
            save_notes(st.session_state.observer_notes)
            st.success("Saved to the observer log.")
            st.rerun()
        else:
            st.warning("Write a note first.")

st.markdown("---")
c_back, c_next = st.columns([1, 1])
if c_back.button("⬅ Back", disabled=(step == 0)):
    st.session_state.step = max(0, step - 1)
    st.rerun()
if c_next.button("Next ➡", disabled=(step == len(steps) - 1)):
    st.session_state.step = min(len(steps) - 1, step + 1)
    st.rerun()

st.caption("Standards in play: 3.MD.C.7 (relate area to multiplication) · 6.EE.A.2c (a formula is an "
           "expression you evaluate) · 6.G.A.1 (composite area).")
st.markdown(
    "<div style='text-align:center;color:#8a939c;font-size:11px;margin-top:18px;'>"
    "www.cognitivecloud.ai &middot; Developed by Xavier Honablue, M.Ed &middot; Chandler Park Academy"
    "</div>",
    unsafe_allow_html=True,
)
