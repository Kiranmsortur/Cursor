# AI Storyteller

A minimal, user-friendly web app to create AI-generated stories for kids.

## Usage Guide

1.  **Open the web app:** Access the app through the provided URL.
2.  **Enter your OpenAI API Key:** The first screen will ask for your OpenAI API key. Enter your key and click "Save Key". Your key will be saved in your browser's local storage for future use.
3.  **Set up Google Cloud Credentials:** This application uses Google's Gemini Pro model for story generation. You need to have your Google Cloud project and credentials configured in your environment. Please follow the instructions in the "Local Setup" section to set up your Google Cloud credentials.
4.  **Create a story:** Fill in the form with the story's title, the child's age, the desired tone, and the language.
5.  **Generate the story:** Click the "Generate Story" button. The app will generate a story and an image.
6.  **Read the story:** The story is displayed in pages. You can navigate through the pages using the "Previous" and "Next" buttons.
7.  **Read Aloud:** Click the "Read Aloud" button to have the current page read to you.
8.  **Download PDF:** Click the "Download PDF" button to download the entire story as a PDF file.

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

3.  **Set up your environment variables:**
    *   **OpenAI API Key:** The application will ask for your OpenAI API key in the UI.
    *   **Google Cloud Credentials:** You need to set up your Google Cloud project and authenticate. The easiest way is to use the `gcloud` CLI.
        - Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
        - Authenticate with your Google account:
          ```bash
          gcloud auth application-default login
          ```
        - Set your project ID:
          ```bash
          gcloud config set project YOUR_PROJECT_ID
          ```
        - The application also needs the `GCP_PROJECT` and `GCP_REGION` environment variables. You can set them in your shell:
          ```bash
          export GCP_PROJECT="YOUR_PROJECT_ID"
          export GCP_REGION="YOUR_GCP_REGION" # e.g., us-central1
          ```

4.  **Run the application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

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
    google-cloud-aiplatform
    openai
    ```

3.  **Push to GitHub:** Push your code to a GitHub repository.

4.  **Deploy from Vercel:**
    - Go to your Vercel dashboard and create a new project.
    - Import your GitHub repository.
    - Vercel should automatically detect the Python framework and configure the build settings.
    - **Add Environment Variables:** In the project settings, add your `GCP_PROJECT` and `GCP_REGION` as environment variables. The `OPENAI_API_KEY` will be provided by the user in the UI.

5.  **Deploy!**
