<<<<<<< HEAD
import os
import re
import json
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="AI Video Summarizer & Quiz Generator",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# GEMINI API SETUP
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("Gemini API key not found.")
    st.info("Create a .env file and add GEMINI_API_KEY.")
    st.stop()

client = genai.Client(api_key=API_KEY)


# ==========================================
# YOUTUBE VIDEO ID
# ==========================================
=======
import re
import random
import streamlit as st
from collections import Counter
from youtube_transcript_api import YouTubeTranscriptApi


# -----------------------------------
# Get YouTube Video ID
# -----------------------------------
>>>>>>> 8156fdcbee95530117a132ad1c409f150e69bf59

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


<<<<<<< HEAD
# ==========================================
# GET TRANSCRIPT
# ==========================================
=======
# -----------------------------------
# Get YouTube Transcript
# -----------------------------------
>>>>>>> 8156fdcbee95530117a132ad1c409f150e69bf59

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


<<<<<<< HEAD
# ==========================================
# GEMINI GENERATION WITH RETRY
# ==========================================

def generate_with_retry(prompt):

    max_attempts = 4

    for attempt in range(max_attempts):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            # Retry temporary server overload
            if "503" in error_message:

                if attempt < max_attempts - 1:

                    wait_time = 5 * (attempt + 1)

                    st.warning(
                        f"Gemini is temporarily busy. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:

                    raise Exception(
                        "Gemini is currently experiencing "
                        "high demand. Please try again after "
                        "a short time."
                    )

            else:

                raise e


# ==========================================
# GENERATE SUMMARY
# ==========================================

def generate_summary(transcript):

    # Keep prompt size reasonable
    transcript = transcript[:50000]

    prompt = f"""
You are an AI educational assistant.

Read the YouTube transcript below.

Create an easy-to-understand summary for a college student.

Include:

1. Main topic
2. Important points
3. Important concepts
4. Short conclusion

Use simple English.

Do not add information that is not present
in the transcript.

TRANSCRIPT:

{transcript}
"""

    return generate_with_retry(prompt)


# ==========================================
# GENERATE QUIZ
# ==========================================

def generate_quiz(transcript):

    transcript = transcript[:50000]

    prompt = f"""
You are an educational quiz generator.

Create exactly 5 multiple-choice questions
from the following YouTube transcript.

Rules:

- Create exactly 5 questions.
- Each question must have 4 options.
- Only one option must be correct.
- Questions must be based on the transcript.
- Use simple English.
- Do not create unrelated questions.

Return ONLY valid JSON.

Use exactly this format:

[
    {{
        "question": "Question text",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "answer": "Correct option"
    }}
]

TRANSCRIPT:

{transcript}
"""

    result = generate_with_retry(prompt)

    # Remove markdown code blocks
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    return json.loads(result)


# ==========================================
# STREAMLIT UI
# ==========================================

st.title("🎓 AI Video Summarizer & Quiz Generator")

st.write(
    "Enter a YouTube educational video URL "
    "to generate an AI summary and quiz."
)


# ==========================================
# INPUT
# ==========================================
=======
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
>>>>>>> 8156fdcbee95530117a132ad1c409f150e69bf59

youtube_url = st.text_input(
    "Enter YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=..."
)


<<<<<<< HEAD
# ==========================================
# GENERATE
# ==========================================

if st.button("Generate Summary & Quiz"):

    if not youtube_url:

        st.warning("Please enter a YouTube URL.")
        st.stop()


    # --------------------------------------
    # VIDEO ID
    # --------------------------------------

    video_id = get_video_id(youtube_url)

    if not video_id:

        st.error("Invalid YouTube URL.")
        st.stop()


    # --------------------------------------
    # TRANSCRIPT
    # --------------------------------------

    with st.spinner("Getting YouTube transcript..."):

        transcript, error = get_transcript(video_id)


    if not transcript:

        st.error("Could not get the YouTube transcript.")

        with st.expander("Technical Error"):
=======
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
>>>>>>> 8156fdcbee95530117a132ad1c409f150e69bf59

            st.code(error)

        st.info(
<<<<<<< HEAD
            "Please try a YouTube video that has "
            "English captions."
=======
            "Try a YouTube video that has "
            "English captions/subtitles."
>>>>>>> 8156fdcbee95530117a132ad1c409f150e69bf59
        )

        st.stop()

<<<<<<< HEAD

    st.success(
        "YouTube transcript obtained successfully!"
    )


    # --------------------------------------
    # SUMMARY
    # --------------------------------------

    with st.spinner("Gemini is creating the summary..."):

        try:

            summary = generate_summary(transcript)

            st.subheader("📚 Video Summary")

            st.write(summary)

        except Exception as e:

            st.error("Could not generate the summary.")

            st.code(str(e))

            st.stop()


    # --------------------------------------
    # QUIZ
    # --------------------------------------

    with st.spinner("Gemini is creating the quiz..."):

        try:

            quiz = generate_quiz(transcript)

            st.subheader("📝 Quiz")


            for i, question in enumerate(quiz, 1):

                st.markdown(
                    f"### Question {i}"
                )

                st.write(
                    question["question"]
                )


                selected = st.radio(
                    "Choose your answer:",
                    question["options"],
                    key=f"question_{i}"
                )


                if st.button(
                    f"Check Answer {i}",
                    key=f"check_{i}"
                ):

                    if selected == question["answer"]:

                        st.success("✅ Correct!")

                    else:

                        st.error(
                            "❌ Incorrect."
                        )

                        st.info(
                            f"Correct answer: "
                            f"{question['answer']}"
                        )


        except json.JSONDecodeError:

            st.error(
                "Gemini returned an invalid quiz format."
            )

        except Exception as e:

            st.error("Could not generate the quiz.")

            st.code(str(e))


# ==========================================
# TRANSCRIPT
# ==========================================

st.divider()

with st.expander("📄 View Transcript"):

    if "transcript" in locals() and transcript:

        st.write(transcript)
=======
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
>>>>>>> 8156fdcbee95530117a132ad1c409f150e69bf59

    else:

        st.write(
<<<<<<< HEAD
            "Generate a summary first to view the transcript."
        )

=======
            "Generate a summary first "
            "to view the transcript."
        )
>>>>>>> 8156fdcbee95530117a132ad1c409f150e69bf59
