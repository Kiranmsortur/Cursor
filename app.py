from flask import Flask, render_template, request, jsonify
import os
import vertexai
from openai import OpenAI
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
)

app = Flask(__name__)

# Configure Gemini API using environment variables
PROJECT_ID = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get("GCP_REGION")
vertexai.init(project=PROJECT_ID, location=LOCATION)

@app.route('/')
def index():
    """Renders the main page of the application."""
    return render_template('index.html')

@app.route('/generate-story', methods=['POST'])
def generate_story_route():
    """
    Handles the story generation request.
    Expects a JSON payload with title, age, tone, language, and openai_api_key.
    Returns a JSON response with the generated story_text and image_url.
    """
    data = request.get_json()

    title = data.get('title')
    age = data.get('age')
    tone = data.get('tone')
    language = data.get('language')
    openai_api_key = data.get('openai_api_key')

    story_prompt = f"Write a short story for a {age}-year-old titled '{title}'. The story should have a {tone} tone and be in {language}."

    # Generate story text using Google Gemini
    text_generation_model = GenerativeModel("gemini-1.0-pro")
    story_text = generate_text(text_generation_model, story_prompt)

    # Generate an image using OpenAI DALL-E 3
    image_prompt = f"A vibrant and imaginative illustration for a children's story titled '{title}'."
    image_url = generate_image(image_prompt, openai_api_key)

    return jsonify({
        'story_text': story_text,
        'image_url': image_url
    })

def generate_text(model, prompt):
    """Generates text using a Google Gemini model."""
    generation_config = {
        "temperature": 0.8,
        "max_output_tokens": 2048,
    }
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
    responses = model.generate_content(
        prompt,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )
    return responses.text

def generate_image(prompt, api_key):
    """Generates an image using OpenAI DALL-E 3."""
    openai_client = OpenAI(api_key=api_key)
    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
