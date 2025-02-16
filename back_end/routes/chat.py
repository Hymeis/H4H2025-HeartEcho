from flask import request, jsonify, session, Blueprint
from openai import OpenAI


# Initialize the OpenAI client
client = OpenAI(api_key="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")

# Store chat history per user
user_sessions = {}

chat_bp = Blueprint('chat', __name__)

def get_response(user_id, user_input):
    """Fetch chat response while maintaining conversation context."""

    # Retrieve or initialize chat history
    if user_id not in user_sessions:
        user_sessions[user_id] = [{"role": "system", "content": "You are a compassionate, empathetic, and non-judgmental mental health mentor designed to provide emotional support, stress management strategies, and wellness advice. "
                                              "Your primary focus is to help users improve their mental well-being, offering active listening, self-care recommendations, and positive reinforcement. Respond in a calm, warm, and supportive tone. "
                                              "Avoid giving medical diagnoses or clinical advice. Guide users toward self-reflection and encourage healthy habits like mindfulness, balanced routines, and seeking professional help when necessary."}]

    # Append user message
    user_sessions[user_id].append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=user_sessions[user_id],
            temperature=0.7,
            max_tokens=512
        )

        # Append assistant response
        assistant_reply = response.choices[0].message.content.strip()
        user_sessions[user_id].append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    except Exception as e:
        return f"An error occurred: {e}"


@chat_bp.route("/", methods=["POST"])
def chat():
    data = request.json
    user_id = data['user_id']  # Unique ID for each user (e.g., session ID)
    user_input = data['user_input']

    if not user_id or not user_input:
        return jsonify({"error": "Missing user_id or message"}), 400

    response = get_response(user_id, user_input)
    return jsonify({"response": response})



