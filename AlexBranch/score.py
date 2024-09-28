import os
from groq import Groq

# Groq API Key setup
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def get_pronunciation_score(theScore, model):

 messages = [
        {
            "role": "system",
            "content": "You are linguistic professor that helps the user become more fluent in the english language. 0 Is a very bad pronunciation. 100 is very good pronunciation. Anything below 50 means its need pronunciation improvement."
        },
        {
            "role": "user",
        "content": f"ScoreInsert:\n{str(theScore)}\n\n----\n\nPrompt: Analyze the score {theScore}, in order to help improve the score of the given input. The goal is to provide suggested feedback on pronunciation improvements.\n"
        },
    ]

 result = client.chat.completions.create(model=model, messages=messages,temperature=0.7, max_tokens=1200);
 return result

theScore = input("Enter Score: ")

result = get_pronunciation_score(theScore, "llama-3.1-70b-versatile");
result_content = result.choices[0].message.content

# Print the Groq Comment Analysis
print(result)
print(result_content)