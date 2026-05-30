from google import genai

client = genai.Client(api_key="AIzaSyB3DZCppyaPwjA8ZL04spMgFDH2Vsb4Z_c")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is coding?"
)

print(response.text)