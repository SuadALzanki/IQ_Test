import streamlit as st
import plotly.graph_objects as go

# ---------- CONFIG ----------
st.set_page_config(page_title="Coursera Interest Quiz", layout="centered")

AXES = ["Data", "Coding", "Design", "Business", "IT/Security", "People/Service"]

# Map each axis to your Coursera role categories (edit anytime)
ROLE_MAP = {
    "Data": [
        "Data Analyst", "Business Intelligence Analyst", "Data Scientist",
        "Data Engineer", "Data Warehouse Developer", "Data Manager",
        "Marketing Analyst", "Supply Chain Analyst", "System Analyst"
    ],
    "Coding": [
        "Python Developer", "Junior Software Developer", "Front-End Developer",
        "Back-End Developer", "Full Stack Developer", "Application Developer",
        "Mobile App Developer", "iOS Developer", "Android Developer",
        "DevOps Engineer"
    ],
    "Design": [
        "UX Designer", "Graphic Designer", "Game Designer",
        "Content Creator", "Social Media Marketer", "Digital Marketing"
    ],
    "Business": [
        "Project Manager", "IT Project Manager", "Program Manager",
        "Product Manager", "Business Analyst", "Technology Consultant",
        "Sales Operations Specialist"
    ],
    "IT/Security": [
        "Cybersecurity Professional", "IT Support Specialist",
        "Network Engineer", "Cloud Support Associate", "Solutions Architect"
    ],
    "People/Service": [
        "Human Resource Specialist", "Recruiter", "Customer service Representative",
        "Career Coach", "Sales Representative", "Sales Development Representative",
        "Public Relations Specialist", "Real Estate Agent", "Insurance Sales Agent"
    ],
}

# ---------- NEW MULTIPLE-CHOICE QUESTIONS ----------
# Format:
# {
#   "prompt": "...",
#   "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
#   "scores":  {"A": {"IT/Security":2}, "B": {"Data":2}, ...}
# }
QUESTIONS = [
    {
        "prompt": "When facing a problem, you usually…",
        "options": {
            "A": "Look for vulnerabilities and risks",
            "B": "Look for patterns and data",
            "C": "Think of creative alternatives",
            "D": "Break it into steps and plan",
        },
        "scores": {
            "A": {"IT/Security": 2},
            "B": {"Data": 2},
            "C": {"Design": 2},
            "D": {"Business": 2},
        },
    },
    {
        "prompt": "Which statement describes you best?",
        "options": {
            "A": "I question systems and don’t trust them easily",
            "B": "I like evidence before decisions",
            "C": "I like expressing ideas visually",
            "D": "I like organizing people and tasks",
        },
        "scores": {
            "A": {"IT/Security": 2},
            "B": {"Data": 2},
            "C": {"Design": 2},
            "D": {"Business": 2, "People/Service": 1},
        },
    },
    {
        "prompt": "You’re organizing a big event. You handle…",
        "options": {
            "A": "Safety and access control",
            "B": "Budget and performance tracking",
            "C": "Posters and promotion",
            "D": "Scheduling and coordination",
        },
        "scores": {
            "A": {"IT/Security": 2},
            "B": {"Data": 2, "Business": 1},
            "C": {"Design": 1, "People/Service": 1},
            "D": {"Business": 2},
        },
    },
    {
        "prompt": "A system suddenly stops working. Your first reaction?",
        "options": {
            "A": "Check security logs and access",
            "B": "Check data and error trends",
            "C": "Think of a user-friendly workaround",
            "D": "Communicate, assign tasks, and track progress",
        },
        "scores": {
            "A": {"IT/Security": 2},
            "B": {"Data": 1, "Coding": 1},
            "C": {"Design": 1, "People/Service": 1},
            "D": {"Business": 2, "People/Service": 1},
        },
    },
    {
        "prompt": "You’re given a group assignment. What role do you naturally take?",
        "options": {
            "A": "Technical checker",
            "B": "Data/analysis person",
            "C": "Designer / presenter",
            "D": "Coordinator / leader",
        },
        "scores": {
            "A": {"IT/Security": 1, "Coding": 1},
            "B": {"Data": 2},
            "C": {"Design": 2},
            "D": {"Business": 2, "People/Service": 1},
        },
    },
    {
        "prompt": "You are given a task with no instructions. What do you do first?",
        "options": {
            "A": "Search examples and documentation",
            "B": "Try things until it works",
            "C": "Sketch ideas or visuals",
            "D": "Break it into steps and plan",
        },
        "scores": {
            "A": {"Coding": 2},
            "B": {"Data": 1, "Coding": 1},
            "C": {"Design": 2},
            "D": {"Business": 2},
        },
    },
    {
        "prompt": "Which statement sounds most like you?",
        "options": {
            "A": "I like finding weaknesses and fixing them",
            "B": "I enjoy numbers and patterns",
            "C": "I enjoy creativity and storytelling",
            "D": "I like planning and organizing",
        },
        "scores": {
            "A": {"IT/Security": 2},
            "B": {"Data": 2},
            "C": {"Design": 2, "People/Service": 1},
            "D": {"Business": 2},
        },
    },
]

def init_state():
    if "idx" not in st.session_state:
        st.session_state.idx = 0
    if "answers" not in st.session_state:
        st.session_state.answers = [None] * len(QUESTIONS)
    if "done" not in st.session_state:
        st.session_state.done = False

def score_answers():
    scores = {a: 0 for a in AXES}
    for i, ans_key in enumerate(st.session_state.answers):
        if ans_key is None:
            continue
        q = QUESTIONS[i]
        axis_weights = q["scores"].get(ans_key, {})
        for axis, pts in axis_weights.items():
            scores[axis] += pts
    return scores

def top_recommendations(scores, top_k=5):
    ranked_axes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    recs = []
    for axis, _ in ranked_axes:
        for r in ROLE_MAP[axis]:
            if r not in recs:
                recs.append(r)
            if len(recs) >= top_k:
                return recs, ranked_axes
    return recs, ranked_axes

def radar_chart(scores):
    values = [scores[a] for a in AXES]
    values += [values[0]]  # close loop
    labels = AXES + [AXES[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values, theta=labels, fill="toself"))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False,
        margin=dict(l=30, r=30, t=30, b=30)
    )
    return fig

# ---------- UI ----------
init_state()

st.title("Find Your Coursera Learning Profile")
st.caption("Quick aptitude & interest quiz (booth version).")

progress = (st.session_state.idx) / len(QUESTIONS)
st.progress(progress)

if not st.session_state.done:
    q = QUESTIONS[st.session_state.idx]
    st.subheader(f"Question {st.session_state.idx + 1} of {len(QUESTIONS)}")

    # Build radio labels like: "A) text"
    labels = [f"{k}) {v}" for k, v in q["options"].items()]
    keys = list(q["options"].keys())

    with st.form("quiz_form", clear_on_submit=False):
        picked_label = st.radio(q["prompt"], labels, index=0)
        submitted = st.form_submit_button("Next")

    if submitted:
        # Convert picked label back to A/B/C/D
        picked_key = picked_label.split(")")[0].strip()
        if picked_key not in keys:
            picked_key = keys[0]

        st.session_state.answers[st.session_state.idx] = picked_key

        if st.session_state.idx < len(QUESTIONS) - 1:
            st.session_state.idx += 1
        else:
            st.session_state.done = True

        st.rerun()

else:
    scores = score_answers()
    recs, ranked_axes = top_recommendations(scores, top_k=5)

    st.success("Your result is ready ✅")

    st.subheader("Top Recommended Tracks")
    for i, r in enumerate(recs[:3], start=1):
        st.write(f"**{i}) {r}**")

    st.subheader("Your Skills Profile (Radar)")
    st.plotly_chart(radar_chart(scores), width="stretch")  # Streamlit current API

    st.subheader("Detailed Axis Scores")
    st.write({k: int(v) for k, v in ranked_axes})

    if st.button("Restart"):
        for k in ["idx", "answers", "done"]:
            st.session_state.pop(k, None)
        st.rerun()
