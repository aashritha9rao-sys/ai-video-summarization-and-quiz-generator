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


# ==========================================
# GET TRANSCRIPT
# ==========================================

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

youtube_url = st.text_input(
    "Enter YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=..."
)


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

            st.code(error)

        st.info(
            "Please try a YouTube video that has "
            "English captions."
        )

        st.stop()


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

    else:

        st.write(
            "Generate a summary first to view the transcript."
        )

