import google.generativeai as genai

from google import genai

def LLM__(content):
    client = genai.Client(api_key="AIzaSyAsJXoYfJRBTGNdr_4fPpM5_n8KYWF1mFw")
    
    
    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=content
        )

        return response.text

    except Exception as e:

        print(e)

        return "⚠️ Model is unable to respond right now. Please try again later."