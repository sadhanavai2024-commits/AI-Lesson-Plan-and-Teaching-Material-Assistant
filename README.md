# AI Lesson Plan & Teaching Material Assistant

A Streamlit app that drafts a lesson plan, worksheet, quiz, homework, six-slide deck outline, visual ideas, and a teacher verification checklist.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

5. Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Enable customized AI generation

Create a Gemini API key from Google AI Studio. Run the app and paste the key into the sidebar, or set `GEMINI_API_KEY` as an environment variable. Do not commit API keys to GitHub.

Without an API key, the app still runs and produces a starter template.

## Deploy and get a public web link

1. Upload `app.py`, `requirements.txt`, and `README.md` to a GitHub repository.
2. Sign in to Streamlit Community Cloud: https://share.streamlit.io/
3. Choose **Create app**, select your repository and `app.py`, then deploy.
4. Add `GEMINI_API_KEY` in the app's **Settings / Secrets** if you want AI generation.
5. Streamlit will provide a public app URL after deployment.

## Responsible AI

AI-generated content can contain errors. A teacher should verify facts, answer keys, curriculum alignment, age suitability, accessibility, and student privacy before classroom use.
