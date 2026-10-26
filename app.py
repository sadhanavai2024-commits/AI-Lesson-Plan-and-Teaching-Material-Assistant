import os
import streamlit as st

st.set_page_config(
    page_title="AI Lesson Plan Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 AI Lesson Plan & Teaching Material Assistant")
st.caption("Create lesson plans, worksheets, quizzes, and homework with AI — with human review before classroom use.")

with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input(
        "Google Gemini API key (optional)",
        type="password",
        help="Add a Gemini API key to generate customized content. You can also set GEMINI_API_KEY in Streamlit secrets.",
    )
    st.info("Always review generated materials for accuracy, syllabus alignment, age suitability, and student privacy.")

st.subheader("1. Set up your lesson")
with st.form("lesson_form"):
    c1, c2 = st.columns(2)
    with c1:
        topic = st.text_input("Lesson topic", placeholder="e.g., Light: Reflection and Refraction")
        subject = st.selectbox(
            "Subject",
            ["Science", "Mathematics", "Computer Science", "English", "Social Science", "Other"],
        )
        target_class = st.text_input("Target class / level", placeholder="e.g., Class 9")
    with c2:
        learning_goal = st.text_area(
            "Learning objectives",
            placeholder="What should learners know or be able to do?",
            height=100,
        )
        prior_knowledge = st.text_input("Prior knowledge (optional)", placeholder="e.g., Basic properties of light")
        lesson_minutes = st.selectbox("Lesson duration", [30, 40, 45, 50, 60], index=2)
    submitted = st.form_submit_button("✨ Generate teaching materials", type="primary", use_container_width=True)

def build_prompt(topic, subject, target_class, learning_goal, prior_knowledge, minutes):
    return f"""
You are a careful teaching assistant. Prepare classroom-ready draft materials.
Subject: {subject}
Topic: {topic}
Target class/level: {target_class}
Duration: {minutes} minutes
Learning objectives: {learning_goal or 'Suggest 2-3 measurable objectives.'}
Prior knowledge: {prior_knowledge or 'Not specified.'}

Return these clearly labeled sections in Markdown:
1. Lesson plan with a minute-by-minute schedule totaling exactly {minutes} minutes, teacher actions, learner actions, and materials.
2. Worksheet with 5 age-appropriate questions.
3. Quiz with 5 questions and an answer key.
4. Homework with 3 tasks.
5. Six-slide teaching deck outline (slide title and 2-3 bullet points per slide).
6. Five classroom visual ideas with descriptions suitable for creating in a free design/image tool.
7. Verification checklist: facts to check, syllabus alignment, age appropriateness, accessibility, and privacy.
8. Human review notes identifying any assumptions or content that needs teacher confirmation.

Use simple, clear language. Do not invent syllabus requirements or cite sources you have not checked.
"""

def fallback_materials(topic, subject, target_class, learning_goal, minutes):
    objectives = learning_goal.strip() or "1. Explain the key idea.\n2. Apply the concept to a simple example.\n3. Answer questions to demonstrate understanding."
    return f"""# Lesson Plan: {topic}

**Subject:** {subject}  
**Target level:** {target_class}  
**Duration:** {minutes} minutes

## Learning objectives
{objectives}

## Lesson plan
| Time | Activity | Teacher and learner actions |
|---|---|---|
| 0–5 min | Starter | Ask a short question to assess prior knowledge. |
| 5–12 min | Introduction | Explain the topic using a simple example. |
| 12–25 min | Teaching and demonstration | Present key concepts; learners take notes and ask questions. |
| 25–35 min | Guided practice | Solve an example together and check understanding. |
| 35–{minutes-5} min | Independent practice | Learners complete a short task or worksheet. |
| {minutes-5}–{minutes} min | Exit ticket | Ask learners to write one thing learned and one remaining question. |

## Worksheet
1. Define **{topic}** in your own words.
2. List two important facts about {topic}.
3. Explain one real-life application of {topic}.
4. Solve or discuss one example related to {topic}.
5. Write one question you still have about {topic}.

## Quiz
1. What is {topic}?
2. State one key fact about the topic.
3. Give one example.
4. Explain why the topic is useful.
5. Write a short summary of what you learned.

### Answer key
Teacher should prepare and verify answers against the approved textbook or syllabus before use.

## Homework
1. Write a short summary of {topic}.
2. Find or draw one real-world example.
3. Prepare two questions to ask in the next class.

## Six-slide teaching deck
1. **Title:** {topic} — introduce the learning goals.
2. **Starter:** Connect the topic to prior knowledge.
3. **Key concept:** Explain the main idea.
4. **Worked example:** Demonstrate an example step by step.
5. **Practice:** Give learners a short activity.
6. **Recap:** Summarize key points and give an exit question.

## Five classroom visual ideas
1. A title poster introducing {topic}.
2. A labeled concept diagram.
3. A step-by-step process infographic.
4. A real-world application illustration.
5. A recap poster showing three key takeaways.

## Verification checklist
- Check all facts against a trusted textbook or syllabus.
- Confirm the material matches the target class.
- Check wording, accessibility, and reading level.
- Remove personal or sensitive student information.
- Teacher review is required before classroom use.

## Human review notes
This is a starter template, not a fully verified lesson. Add curriculum-specific content and confirm the answer key before teaching.
"""

if submitted:
    if not topic.strip() or not target_class.strip():
        st.error("Please enter a lesson topic and target class/level.")
    else:
        prompt = build_prompt(topic.strip(), subject, target_class.strip(), learning_goal, prior_knowledge, lesson_minutes)
        secret_key = api_key.strip() or os.getenv("GEMINI_API_KEY")
        if not secret_key:
            try:
                secret_key = st.secrets.get("GEMINI_API_KEY", "")
            except Exception:
                secret_key = ""

        result = None
        if secret_key:
            try:
                from google import genai
                client = genai.Client(api_key=secret_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                result = response.text
                if not result:
                    st.warning("The AI returned an empty response. Showing a starter template instead.")
            except Exception as exc:
                st.warning(f"AI generation could not complete ({exc}). Showing a starter template instead.")
        else:
            st.info("No Gemini API key provided, so a starter template is shown. Add a key in the sidebar for customized AI-generated materials.")

        if not result:
            result = fallback_materials(topic.strip(), subject, target_class.strip(), learning_goal, lesson_minutes)

        st.session_state["lesson_output"] = result
        st.session_state["lesson_topic"] = topic.strip()

if "lesson_output" in st.session_state:
    st.divider()
    st.subheader(f"2. Your teaching materials: {st.session_state.get('lesson_topic', '')}")
    st.markdown(st.session_state["lesson_output"])
    st.download_button(
        "⬇️ Download materials as Markdown",
        data=st.session_state["lesson_output"],
        file_name="lesson_materials.md",
        mime="text/markdown",
        use_container_width=True,
    )
    st.caption("Before using this material, verify facts, syllabus alignment, age appropriateness, and all answer keys.")
else:
    st.markdown("---")
    st.markdown("### What this app creates")
    a, b, c = st.columns(3)
    a.metric("Lesson plan", "Timed")
    b.metric("Practice", "Worksheet + quiz")
    c.metric("Teaching aid", "6-slide outline")
    st.write("Fill in the lesson details above and select **Generate teaching materials** to get started.")
