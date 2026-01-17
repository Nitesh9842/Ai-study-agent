from groq import Groq
from groq.types.chat import ChatCompletionMessageParam
from config import Config
from typing import Dict, List, Optional, cast


class OutputGenerator:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.system_prompt = """You are an AI Study Buddy, a helpful and encouraging educational assistant. 
Your goal is to help students learn effectively by:
- Explaining concepts clearly and concisely
- Adapting to the student's level
- Providing examples and analogies
- Encouraging curiosity and deeper understanding
- Being patient and supportive

Always be accurate, helpful, and engaging."""

    def generate_response(self, plan: Dict, context: Optional[List] = None) -> str:
        """Generate a response based on the task plan."""
        messages: List[ChatCompletionMessageParam] = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation context if available
        if context:
            for entry in context[-3:]:  # Last 3 interactions
                messages.append({"role": "user", "content": entry.get("user_input", "")})
                messages.append({"role": "assistant", "content": entry.get("response", "")})
        
        # Add the current request
        messages.append({"role": "user", "content": plan["prompt_template"]})
        
        response = self.client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=messages,
            max_tokens=Config.MAX_TOKENS,
            temperature=Config.TEMPERATURE
        )
        
        return response.choices[0].message.content or ""
    
    def format_response(self, response: str, task_type: str) -> str:
        """Format the response based on task type."""
        headers = {
            "explanation": "📚 Explanation",
            "summary": "📝 Summary",
            "quiz": "❓ Quiz Time",
            "definition": "📖 Definition",
            "comparison": "⚖️ Comparison",
            "practice": "✏️ Practice",
            "general": "💡 Response"
        }
        
        header = headers.get(task_type, "💡 Response")
        return f"\n{header}\n{'='*40}\n{response}\n"
