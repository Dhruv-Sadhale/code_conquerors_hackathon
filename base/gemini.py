import google.generativeai as genai
from django.conf import settings

# Configure API key
genai.configure(api_key=settings.GEMINI_API_KEY)

# Generate Text from Gemini API
def generate_text(prompt):
    try:
        model_name = "models/gemini-1.5-flash-002"
        model = genai.GenerativeModel(model_name)  # Using Gemini Pro model
        response = model.generate_content(prompt)
        if response.text:
            gemini_response = response.text  # Store response in a variable
            return gemini_response
        else:
            return "No response generated. Try again."
    except Exception as e:
        return f"Error: {str(e)}"
