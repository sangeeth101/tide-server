from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os

app = Flask(__name__)
CORS(app)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

@app.route('/plan', methods=['POST'])
def plan():
    tasks = request.json["tasks"]

    lines = "\n".join(
        f"- {t}" for t in tasks
    )

    try:
        response = client.models.generate_content(
            model="models/gemini-2.0-flash",
            contents=
                f"You are Tide's planning assistant. Be concise.\n"
                f"Order these tasks by urgency, one reason each:\n{lines}"
        )

        text = response.text

    except Exception as e:
        text = f"Error: {str(e)}"

    return jsonify({
        "plan": text
    })

    
if __name__ == '__main__':
    port=int(os.environ.get('PORT') or 5000)
    app.run(debug=False, host='0.0.0.0',port=port)