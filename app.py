<<<<<<< HEAD
import streamlit as st
import re
import random
=======
import re
import streamlit as st
>>>>>>> f0fc731d416b8c488ebf4b901fd1f5d29f7155de
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(
    page_title="AI Video Summarizer & Quiz Generator",
    page_icon="🎓"
)

<<<<<<< HEAD
st.title("🎓 AI Video Summarizer & Quiz Generator")

st.write(
    "Enter a YouTube video URL to generate a summary "
    "and quiz without an API key or FFmpeg."
)


# -----------------------------
# GET YOUTUBE VIDEO ID
# -----------------------------

def get_video_id(url):

    patterns = [
        r"(?:youtube\.com/watch\?v=)([^&]+)",
        r"(?:youtu\.be/)([^?]+)",
        r"(?:youtube\.com/shorts/)([^?]+)",
        r"(?:youtube\.com/embed/)([^?]+)"
    ]

    for pattern in patterns:

=======

def get_video_id(url):
    patterns = [
        r"youtube\.com/watch\?v=([^&]+)",
        r"youtu\.be/([^?]+)",
        r"youtube\.com/embed/([^?]+)",
        r"youtube\.com/shorts/([^?]+)"
    ]

    for pattern in patterns:
>>>>>>> f0fc731d416b8c488ebf4b901fd1f5d29f7155de
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    return None


<<<<<<< HEAD
# -----------------------------
# GET TRANSCRIPT
# -----------------------------

def get_transcript(video_id):

    api = YouTubeTranscriptApi()

    transcript = api.fetch(
        video_id,
        languages=["en", "en-US", "en-GB"]
    )

    text = " ".join(
        item.text for item in transcript
    )

    return text


# -----------------------------
# SPLIT SENTENCES
# -----------------------------

def split_sentences(text):

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
=======
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
>>>>>>> f0fc731d416b8c488ebf4b901fd1f5d29f7155de
        s.strip()
        for s in sentences
        if len(s.strip()) > 30
    ]

<<<<<<< HEAD

# -----------------------------
# CREATE SUMMARY
# -----------------------------

def create_summary(text):

    sentences = split_sentences(text)

    if not sentences:
        return text[:2000]

    keywords = [
        "important",
        "means",
        "defined",
        "called",
        "used",
        "system",
        "database",
        "information",
        "process",
        "data",
        "computer"
    ]

    scored_sentences = []

    for sentence in sentences:

        score = 0

        lower = sentence.lower()

        for keyword in keywords:

            if keyword in lower:
                score += 1

        scored_sentences.append(
            (score, sentence)
        )

    scored_sentences.sort(
        key=lambda x: x[0],
        reverse=True
    )

    summary = " ".join(
        sentence
        for score, sentence
        in scored_sentences[:8]
    )
=======
    if not sentences:
        return text[:2000]

    # Take important sentences from the transcript
    selected = sentences[:8]

    summary = " ".join(selected)
>>>>>>> f0fc731d416b8c488ebf4b901fd1f5d29f7155de

    return summary


<<<<<<< HEAD
# -----------------------------
# CREATE QUIZ
# -----------------------------

def create_quiz(text):

    sentences = split_sentences(text)

    quiz = []

    for sentence in sentences:
=======
def create_quiz(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    sentences = [
        s.strip()
        for s in sentences
        if len(s.strip()) > 40
    ]

    quiz = []

    for sentence in sentences[:5]:
>>>>>>> f0fc731d416b8c488ebf4b901fd1f5d29f7155de

        words = sentence.split()

        if len(words) < 8:
            continue

<<<<<<< HEAD
        candidates = [
            word.strip(".,!?;:()[]")
            for word in words
            if len(word.strip(".,!?;:()[]")) > 5
        ]

        if not candidates:
            continue

        answer = candidates[-1]

        question = sentence.replace(
=======
        answer = words[-1].strip(".,!?")

        question_text = sentence.replace(
>>>>>>> f0fc731d416b8c488ebf4b901fd1f5d29f7155de
            answer,
            "_____",
            1
        )

<<<<<<< HEAD
        wrong_answers = [
            "Computer",
            "Database",
            "Network",
            "Software",
            "Information",
            "System"
        ]

        wrong_answers = [
            x for x in wrong_answers
            if x.lower() != answer.lower()
        ]

        random.shuffle(wrong_answers)

        options = [
            answer,
            wrong_answers[0],
            wrong_answers[1],
            wrong_answers[2]
        ]

        random.shuffle(options)

        quiz.append({
            "question": question,
=======
        options = [
            answer,
            "Database",
            "Computer",
            "System"
        ]

        quiz.append({
            "question": question_text,
>>>>>>> f0fc731d416b8c488ebf4b901fd1f5d29f7155de
            "options": options,
            "answer": answer
        })

<<<<<<< HEAD
        if len(quiz) == 5:
            break

    return quiz


# -----------------------------
# URL INPUT
# -----------------------------

youtube_url = st.text_input(
    "🔗 Enter YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=..."
)


# -----------------------------
# GENERATE
# -----------------------------

if st.button(
    "🚀 Generate Summary & Quiz",
    type="primary"
):

    if not youtube_url:

        st.warning(
            "Please enter a YouTube URL."
        )

        st.stop()

    video_id = get_video_id(
        youtube_url
    )

    if not video_id:

        st.error(
            "Invalid YouTube URL."
        )

        st.stop()

    try:

        with st.spinner(
            "Getting video transcript..."
        ):

            transcript = get_transcript(
                video_id
            )

        if not transcript:

            st.error(
                "No transcript was found."
            )

            st.stop()

        st.success(
            "Transcript obtained successfully!"
        )

        # -------------------------
        # SUMMARY
        # -------------------------

        with st.spinner(
            "Generating summary..."
        ):

            summary = create_summary(
                transcript
            )

        st.subheader(
            "📚 Video Summary"
        )

        st.write(summary)

        # -------------------------
        # QUIZ
        # -------------------------

        quiz = create_quiz(
            transcript
        )

        st.subheader(
            "📝 Quiz"
        )

        if not quiz:

            st.warning(
                "Could not generate quiz questions."
            )

        else:

            score = 0

            for i, q in enumerate(
                quiz,
                start=1
            ):

                st.markdown(
                    f"### Question {i}"
                )

                st.write(
                    q["question"]
                )

                selected = st.radio(
                    "Choose your answer:",
                    q["options"],
                    key=f"question_{i}"
                )

                if st.button(
                    f"Check Answer {i}",
                    key=f"check_{i}"
                ):

                    if selected == q["answer"]:

                        st.success(
                            "✅ Correct!"
                        )

                        score += 1

                    else:

                        st.error(
                            "❌ Incorrect!"
                        )

                        st.info(
                            f"Correct answer: "
                            f"{q['answer']}"
                        )

            # -------------------------
            # TRANSCRIPT
            # -------------------------

            with st.expander(
                "📄 View Transcript"
            ):

                st.write(transcript)

    except Exception as e:

        st.error(
            "Could not get the transcript."
        )

        st.info(
            "Make sure the video has English "
            "captions/transcript."
        )

        st.caption(
            f"Details: {e}"
        )
=======
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
           
>>>>>>> f0fc731d416b8c488ebf4b901fd1f5d29f7155de
