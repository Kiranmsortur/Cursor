from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main page of the application."""
    return render_template('index.html')

@app.route('/generate-story', methods=['POST'])
def generate_story_route():
    """
    Handles the story generation request.
    Expects a JSON payload with title, age, tone, language, gemini_api_key, and model.
    Returns a JSON response with the generated story_text.
    """
    data = request.get_json()

    title = data.get('title')
    age = data.get('age')
    tone = data.get('tone')
    language = data.get('language')
    gemini_api_key = data.get('gemini_api_key')
    model = data.get('model') # 'gemini-2.5-pro' or 'gemini-2.5-flash'

    story_prompt = f"Write a short story for a {age}-year-old titled '{title}'. The story should have a {tone} tone and be in {language}."

    try:
        genai.configure(api_key=gemini_api_key)

        generation_config = {
            "temperature": 0.8,
            "max_output_tokens": 2048,
        }

        model_instance = genai.GenerativeModel(model)
        response = model_instance.generate_content(
            story_prompt,
            generation_config=generation_config,
        )

        return jsonify({
            'story_text': response.text
        })
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
