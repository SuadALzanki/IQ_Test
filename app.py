import streamlit as st
import plotly.graph_objects as go

# ---------- CONFIG ----------
st.set_page_config(page_title="Coursera Interest Quiz", layout="centered")

AXES = ["Data", "Coding", "Design", "Business", "IT/Security", "People/Service"]

# Map each axis to your Coursera role categories (you can edit anytime)
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

# Each question adds points to axes
QUESTIONS = [
    ("I enjoy working with numbers, reports, or trends.", {"Data": 2, "Business": 1}),
    ("I like building things with code or debugging problems.", {"Coding": 2, "IT/Security": 1}),
    ("I enjoy making visuals, layouts, or improving user experience.", {"Design": 2}),
    ("I like planning tasks, organizing people, and managing timelines.", {"Business": 2, "People/Service": 1}),
    ("I’m interested in networks, security, or IT systems.", {"IT/Security": 2, "Coding": 1}),
    ("I prefer roles that involve communication, advising, or customer interaction.", {"People/Service": 2, "Business": 1}),
]

OPTIONS = {
    "Strongly disagree": 0,
    "Disagree": 1,
    "Neutral": 2,
    "Agree": 3,
    "Strongly agree": 4,
}

def init_state():
    if "idx" not in st.session_state:
        st.session_state.idx = 0
    if "answers" not in st.session_state:
        st.session_state.answers = [None] * len(QUESTIONS)
    if "done" not in st.session_state:
        st.session_state.done = False

def score_answers():
    scores = {a: 0 for a in AXES}
    for i, ans in enumerate(st.session_state.answers):
        if ans is None:
            continue
        weight = OPTIONS[ans]
        _, axis_weights = QUESTIONS[i]
        for axis, pts in axis_weights.items():
            scores[axis] += pts * weight
    return scores

def top_recommendations(scores, top_k=3):
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
    # Close the loop for radar
    values += [values[0]]
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
st.progress(progress)  # Streamlit progress bar  [oai_citation:4‡Streamlit Docs](https://docs.streamlit.io/develop/api-reference/status/st.progress?utm_source=chatgpt.com)

if not st.session_state.done:
    q_text, _ = QUESTIONS[st.session_state.idx]
    st.subheader(f"Question {st.session_state.idx + 1} of {len(QUESTIONS)}")
    with st.form("quiz_form", clear_on_submit=False):
        choice = st.radio(q_text, list(OPTIONS.keys()), index=2)
        submitted = st.form_submit_button("Next")

    if submitted:
        st.session_state.answers[st.session_state.idx] = choice
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
    st.plotly_chart(radar_chart(scores), use_container_width=True)  # Plotly radar  [oai_citation:5‡plotly.com](https://plotly.com/python/radar-chart/?utm_source=chatgpt.com)

    st.subheader("Detailed Axis Scores")
    st.write({k: int(v) for k, v in ranked_axes})

    if st.button("Restart"):
        for k in ["idx", "answers", "done"]:
            st.session_state.pop(k, None)
        st.rerun()
