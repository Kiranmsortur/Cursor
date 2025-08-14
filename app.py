from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI, APIError

app = Flask(__name__)

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

    try:
        # Generate story text using OpenAI GPT
        story_text = generate_text_openai(story_prompt, openai_api_key)

        # Generate an image using OpenAI DALL-E 3
        image_prompt = f"A vibrant and imaginative illustration for a children's story titled '{title}'."
        image_url = generate_image(image_prompt, openai_api_key)

        return jsonify({
            'story_text': story_text,
            'image_url': image_url
        })
    except APIError as e:
        return jsonify({"error": f"An error occurred with the OpenAI API: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

def generate_text_openai(prompt, api_key):
    """Generates text using an OpenAI model."""
    openai_client = OpenAI(api_key=api_key)
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative storyteller for children."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=2048,
    )
    return response.choices[0].message.content

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
