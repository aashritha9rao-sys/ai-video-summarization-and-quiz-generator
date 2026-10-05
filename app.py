import re
import random
import streamlit as st
from collections import Counter
from youtube_transcript_api import YouTubeTranscriptApi


# -----------------------------------
# Get YouTube Video ID
# -----------------------------------

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


# -----------------------------------
# Get YouTube Transcript
# -----------------------------------

def get_transcript(video_id):

    try:

        api = YouTubeTranscriptApi()

        transcript = api.fetch(
            video_id,
            languages=["en", "en-US", "en-GB"]
        )

        text = " ".join(
            item.text for item in transcript
        )

        return text, None

    except Exception as e:

        return None, str(e)


# -----------------------------------
# Clean Text
# -----------------------------------

def clean_text(text):

    text = re.sub(
        r"\[[^\]]*\]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# -----------------------------------
# Local Summary
# -----------------------------------

def generate_local_summary(transcript):

    transcript = clean_text(transcript)

    sentences = re.split(
        r"(?<=[.!?])\s+",
        transcript
    )

    sentences = [
        s.strip()
        for s in sentences
        if len(s.strip()) > 40
    ]

    if not sentences:
        return transcript[:1000]

    # Words to ignore
    stop_words = {
        "this", "that", "with", "from", "have",
        "they", "their", "there", "which", "about",
        "would", "could", "should", "where",
        "when", "what", "your", "you", "into",
        "also", "will", "then", "than", "these",
        "those", "been", "were", "being", "because",
        "very", "more", "some", "such", "just",
        "like", "using", "used", "it's"
    }

    words = re.findall(
        r"\b[a-zA-Z]{4,}\b",
        transcript.lower()
    )

    words = [
        word
        for word in words
        if word not in stop_words
    ]

    frequency = Counter(words)

    # Score sentences
    scored_sentences = []

    for sentence in sentences:

        sentence_words = re.findall(
            r"\b[a-zA-Z]{4,}\b",
            sentence.lower()
        )

        score = sum(
            frequency[word]
            for word in sentence_words
        )

        scored_sentences.append(
            (score, sentence)
        )

    # Sort by score
    scored_sentences.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    # Select top 5 sentences
    selected = [
        sentence
        for score, sentence
        in scored_sentences[:5]
    ]

    return " ".join(selected)


# -----------------------------------
# Find Important Words
# -----------------------------------

def get_keywords(transcript):

    stop_words = {
        "this", "that", "with", "from", "have",
        "they", "their", "there", "which", "about",
        "would", "could", "should", "where",
        "when", "what", "your", "you", "into",
        "also", "will", "then", "than", "these",
        "those", "been", "were", "being", "because",
        "very", "more", "some", "such", "just",
        "like", "using", "used", "video", "today",
        "going", "really", "make", "made"
    }

    words = re.findall(
        r"\b[a-zA-Z]{5,}\b",
        transcript.lower()
    )

    words = [
        word
        for word in words
        if word not in stop_words
    ]

    frequency = Counter(words)

    return [
        word
        for word, count
        in frequency.most_common(30)
    ]


# -----------------------------------
# Generate Local Quiz
# -----------------------------------

def generate_quiz(
    transcript,
    number_of_questions=5
):

    transcript = clean_text(transcript)

    sentences = re.split(
        r"(?<=[.!?])\s+",
        transcript
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if len(sentence) > 60
    ]

    keywords = get_keywords(transcript)

    questions = []

    used_words = set()

    for sentence in sentences:

        if len(questions) >= number_of_questions:
            break

        sentence_lower = sentence.lower()

        # Find an important word
        answer = None

        for word in keywords:

            if word in used_words:
                continue

            if re.search(
                r"\b" + re.escape(word) + r"\b",
                sentence_lower
            ):

                answer = word
                break

        if not answer:
            continue

        used_words.add(answer)

        # Replace answer with blank
        pattern = re.compile(
            r"\b" + re.escape(answer) + r"\b",
            re.IGNORECASE
        )

        question_text = pattern.sub(
            "________",
            sentence,
            count=1
        )

        # Create wrong answers
        wrong_answers = []

        for word in keywords:

            if (
                word != answer
                and word not in wrong_answers
                and word not in used_words
            ):

                wrong_answers.append(word)

            if len(wrong_answers) == 3:
                break

        if len(wrong_answers) < 3:
            continue

        # Create options
        options = [
            answer,
            wrong_answers[0],
            wrong_answers[1],
            wrong_answers[2]
        ]

        # Shuffle options
        random.shuffle(options)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })

    return questions


# -----------------------------------
# Streamlit Page
# -----------------------------------

st.set_page_config(
    page_title="AI Video Summarizer & Quiz Generator",
    page_icon="🎓",
    layout="wide"
)


# -----------------------------------
# Title
# -----------------------------------

st.title(
    "🎓 Video Summarizer & Quiz Generator"
)

st.write(
    "Generate a summary and quiz from a "
    "YouTube educational video."
)


# -----------------------------------
# YouTube URL
# -----------------------------------

youtube_url = st.text_input(
    "Enter YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=..."
)


# -----------------------------------
# Generate Button
# -----------------------------------

if st.button("Generate Summary & Quiz"):

    # Check URL
    if not youtube_url:

        st.warning(
            "Please enter a YouTube URL."
        )

        st.stop()

    # Get video ID
    video_id = get_video_id(
        youtube_url
    )

    if not video_id:

        st.error(
            "Invalid YouTube URL."
        )

        st.stop()

    # -----------------------------------
    # Get Transcript
    # -----------------------------------

    with st.spinner(
        "Getting YouTube transcript..."
    ):

        transcript, error = get_transcript(
            video_id
        )

    if not transcript:

        st.error(
            "Could not get the transcript."
        )

        with st.expander(
            "Technical Error"
        ):

            st.code(error)

        st.info(
            "Try a YouTube video that has "
            "English captions/subtitles."
        )

        st.stop()

    st.success(
        "Transcript obtained successfully!"
    )


    # -----------------------------------
    # Generate Summary
    # -----------------------------------

    with st.spinner(
        "Creating summary..."
    ):

        summary = generate_local_summary(
            transcript
        )

    st.subheader(
        "📚 Video Summary"
    )

    st.write(summary)


    # -----------------------------------
    # Generate Quiz
    # -----------------------------------

    with st.spinner(
        "Creating quiz..."
    ):

        quiz = generate_quiz(
            transcript,
            number_of_questions=5
        )

    st.subheader(
        "📝 Quiz"
    )

    if not quiz:

        st.warning(
            "Could not create quiz questions "
            "from this transcript."
        )

    else:

        for i, q in enumerate(
            quiz,
            1
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

                else:

                    st.error(
                        f"❌ Incorrect. "
                        f"Correct answer: {q['answer']}"
                    )


# -----------------------------------
# View Transcript
# -----------------------------------

st.divider()

with st.expander(
    "View Transcript"
):

    if (
        "transcript" in locals()
        and transcript
    ):

        st.write(
            transcript
        )

    else:

        st.write(
            "Generate a summary first "
            "to view the transcript."
        )