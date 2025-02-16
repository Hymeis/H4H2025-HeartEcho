import os

if "OPENAI_API_KEY" in os.environ:
    print("API_KEY is set!")
else:
    print("API_KEY is missing.")