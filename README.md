# AI Storyteller

A minimal, user-friendly web app to create AI-generated stories for kids using Google's Gemini models.

## Usage Guide

1.  **Open the web app:** Access the app through the provided URL.
2.  **Enter your Gemini API Key:** The first screen will ask for your Google Gemini API key. You can get a key from [Google AI Studio](https://aistudio.google.com/app/apikey). Enter your key and click "Save Key". Your key will be saved in your browser's local storage for future use.
3.  **Create a story:**
    *   Select the Gemini model you want to use (Pro or Flash).
    *   Fill in the form with the story's title, the child's age, the desired tone, and the language.
4.  **Generate the story:** Click the "Generate Story" button. The app will generate a story for you.
5.  **Read the story:** The story is displayed in pages. You can navigate through the pages using the "Previous" and "Next" buttons.
6.  **Read Aloud:** Click the "Read Aloud" button to have the current page read to you.
7.  **Download PDF:** Click the "Download PDF" button to download the entire story as a PDF file.

## Local Setup

To run the application locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`. The app will ask for your Gemini API key in the UI.

## Deployment to Vercel

1.  **Create a `vercel.json` file:** This file tells Vercel how to build and run the application. Create a file named `vercel.json` with the following content:
    ```json
    {
      "builds": [
        {
          "src": "app.py",
          "use": "@vercel/python",
          "config": { "maxLambdaSize": "15mb", "runtime": "python3.9" }
        }
      ],
      "routes": [
        {
          "src": "/(.*)",
          "dest": "app.py"
        }
      ]
    }
    ```

2.  **Update `requirements.txt`:** Make sure your `requirements.txt` file contains the following:
    ```
    Flask
    google-generativeai
    ```

3.  **Push to GitHub:** Push your code to a GitHub repository.

4.  **Deploy from Vercel:**
    - Go to your Vercel dashboard and create a new project.
    - Import your GitHub repository.
    - Vercel should automatically detect the Python framework and configure the build settings.
    - No environment variables are needed for the deployment, as the Gemini API key is provided by the user in the UI.

5.  **Deploy!**
