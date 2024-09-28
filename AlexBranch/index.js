import Groq from "groq-sdk";
import readline from "readline";

// Groq API Key setup
// Set the Groq API key (it’s better to set this in an .env file)
process.env.GROQ_API_KEY = "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";

// Initialize Groq client with the API key
const client = new Groq({ apiKey: process.env.GROQ_API_KEY });

async function getPronunciationScore(theScore, model) {
    const messages = [
        {
            role: "system",
            content:
                "You are a linguistic professor that helps the user become more fluent in the English language. 0 is a very bad pronunciation. 100 is very good pronunciation. Anything below 50 means it needs pronunciation improvement.",
        },
        {
            role: "user",
            content: `ScoreInsert:\n${theScore}\n\n----\n\nPrompt: Analyze the score ${theScore}, in order to help improve the score of the given input. The goal is to provide suggested feedback on pronunciation improvements.\n`,
        },
    ];

    const result = await client.chat.completions.create({
        model: model,
        messages: messages,
        temperature: 0.7,
        max_tokens: 1200,
    });

    return result;
}

// Input setup to take score from the user
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

rl.question("Enter Score: ", async (theScore) => {
    try {
        const result = await getPronunciationScore(theScore, "llama-3.1-70b-versatile");
        const resultContent = result.choices[0]?.message?.content || "No content received";

        // Print the Groq Comment Analysis
        console.log(result);
        console.log(resultContent);
    } catch (error) {
        console.error("Error occurred:", error);
    }

    rl.close();
});

