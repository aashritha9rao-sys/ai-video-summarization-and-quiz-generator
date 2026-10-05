import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(
    page_title="AI Video Summarizer & Quiz Generator",
    page_icon="🎓"
)


def get_video_id(url):
    patterns = [
        r"youtube\.com/watch\?v=([^&]+)",
        r"youtu\.be/([^?]+)",
        r"youtube\.com/embed/([^?]+)",
        r"youtube\.com/shorts/([^?]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    return None


def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()

        transcript = api.fetch(
            video_id,
            languages=["en", "en-US", "en-GB"]
        )

        text = " ".join(item.text for item in transcript)

        return text

    except Exception as e:
        return None


def create_summary(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    sentences = [
        s.strip()
        for s in sentences
        if len(s.strip()) > 30
    ]

    if not sentences:
        return text[:2000]

    # Take important sentences from the transcript
    selected = sentences[:8]

    summary = " ".join(selected)

    return summary


def create_quiz(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    sentences = [
        s.strip()
        for s in sentences
        if len(s.strip()) > 40
    ]

    quiz = []

    for sentence in sentences[:5]:

        words = sentence.split()

        if len(words) < 8:
            continue

        answer = words[-1].strip(".,!?")

        question_text = sentence.replace(
            answer,
            "_____",
            1
        )

        options = [
            answer,
            "Database",
            "Computer",
            "System"
        ]

        quiz.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })

    return quiz[:5]


st.title("🎓 AI Video Summarizer & Quiz Generator")

st.write(
    "Enter a YouTube educational video URL "
    "to generate a summary and quiz."
)

youtube_url = st.text_input(
    "Enter YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

if st.button("Generate Summary & Quiz", type="primary"):

    if not youtube_url:
        st.warning("Please enter a YouTube URL.")
        st.stop()

    video_id = get_video_id(youtube_url)

    if not video_id:
        st.error("Invalid YouTube URL.")
        st.stop()

    with st.spinner("Getting YouTube transcript..."):

        transcript = get_transcript(video_id)

    if not transcript:

        st.error(
            "Could not get the YouTube transcript."
        )

        st.info(
            "Please try a video with English captions."
        )

        st.stop()

    st.success(
        "YouTube transcript obtained successfully!"
    )

    with st.spinner("Creating summary and quiz..."):

        summary = create_summary(transcript)

        quiz = create_quiz(transcript)

    st.subheader("📚 Video Summary")

    st.write(summary)

    st.subheader("📝 Quiz")

    if not quiz:

        st.warning(
            "Could not create quiz questions from this transcript."
        )

    else:

        for i, question in enumerate(
            quiz,
            start=1
        ):

            st.markdown(
                f"### Question {i}"
            )

            st.write(
                question["question"]
            )

            selected = st.radio(
                "Choose your answer:",
                question["options"],
                key=f"answer_{i}"
            )

            if st.button(
                f"Check Answer {i}",
                key=f"check_{i}"
            ):

                if selected == question["answer"]:

                    st.success("✅ Correct!")

                else:

                    st.error("❌ Incorrect!")

                    st.info(
                        f"Correct answer: "
                        f"{question['answer']}"
                    )

    with st.expander("📄 View Transcript"):

        st.write(transcript)
           