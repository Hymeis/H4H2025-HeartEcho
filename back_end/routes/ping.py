import os
from openai import OpenAI

key = "YOUR KEY"
client = OpenAI(api_key=key)

#print("OpenAI library version:", openai.__version__)

def check_available_models():
    """Check if GPT-4 is available for the provided API key."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Test message"}],
            max_tokens=5
        )
        #print("GPT-4 is available for your API key.")
        return True

    except Exception as e:
        #print(f"GPT-4 is NOT available. Error: {e}")
        return False


def get_response(user_input):
    """Sends a request to OpenAI API with a custom system message and user input."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a compassionate, empathetic, and non-judgmental mental health mentor designed to provide emotional support, stress management strategies, and wellness advice. "
                                              "Your primary focus is to help users improve their mental well-being, offering active listening, self-care recommendations, and positive reinforcement. Respond in a calm, warm, and supportive tone. "
                                              "Avoid giving medical diagnoses or clinical advice. Guide users toward self-reflection and encourage healthy habits like mindfulness, balanced routines, and seeking professional help when necessary."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=512
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    check_available_models()
    print("Welcome to the Mental Health Mentor!")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! Take care. 😊")
            break
        response = get_response(user_input)
        print(f"Mental Health Mentor: {response}")