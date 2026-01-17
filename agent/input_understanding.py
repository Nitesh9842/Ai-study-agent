from groq import Groq
from config import Config


class InputUnderstanding:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
    
    def parse_input(self, user_input: str) -> dict:
        """Parse user input to extract intent and entities."""
        prompt = f"""Analyze the following study-related query and extract:
1. intent (e.g., explain, summarize, quiz, define, compare)
2. topic (the main subject)
3. difficulty_level (beginner, intermediate, advanced)
4. specific_request (any specific details requested)

User query: {user_input}

Respond in JSON format only."""

        response = self.client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3
        )
        
        return {
            "raw_input": user_input,
            "parsed": response.choices[0].message.content
        }
    
    def classify_intent(self, user_input: str) -> str:
        """Classify the primary intent of the user."""
        intents = ["explain", "summarize", "quiz", "define", "compare", "practice", "general"]
        
        input_lower = user_input.lower()
        if "explain" in input_lower or "how" in input_lower:
            return "explain"
        elif "summarize" in input_lower or "summary" in input_lower:
            return "summarize"
        elif "quiz" in input_lower or "test" in input_lower:
            return "quiz"
        elif "define" in input_lower or "what is" in input_lower:
            return "define"
        elif "compare" in input_lower or "difference" in input_lower:
            return "compare"
        elif "practice" in input_lower or "exercise" in input_lower:
            return "practice"
        return "general"
