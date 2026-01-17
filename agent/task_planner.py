from typing import List, Dict


class TaskPlanner:
    def __init__(self):
        self.task_templates = {
            "explain": self._plan_explanation,
            "summarize": self._plan_summary,
            "quiz": self._plan_quiz,
            "define": self._plan_definition,
            "compare": self._plan_comparison,
            "practice": self._plan_practice,
            "general": self._plan_general
        }
    
    def create_plan(self, intent: str, topic: str, difficulty: str) -> Dict:
        """Create an execution plan based on intent."""
        planner = self.task_templates.get(intent, self._plan_general)
        return planner(topic, difficulty)
    
    def _plan_explanation(self, topic: str, difficulty: str) -> Dict:
        return {
            "task_type": "explanation",
            "steps": [
                "Provide a clear definition",
                "Explain core concepts",
                "Give real-world examples",
                "Summarize key points"
            ],
            "prompt_template": f"Explain {topic} at a {difficulty} level. Include definition, core concepts, examples, and key takeaways."
        }
    
    def _plan_summary(self, topic: str, difficulty: str) -> Dict:
        return {
            "task_type": "summary",
            "steps": [
                "Identify main points",
                "Condense information",
                "Highlight key takeaways"
            ],
            "prompt_template": f"Provide a concise summary of {topic} suitable for a {difficulty} learner."
        }
    
    def _plan_quiz(self, topic: str, difficulty: str) -> Dict:
        return {
            "task_type": "quiz",
            "steps": [
                "Generate questions",
                "Provide multiple choice options",
                "Include correct answers"
            ],
            "prompt_template": f"Create a {difficulty} level quiz about {topic} with 5 questions. Include answers."
        }
    
    def _plan_definition(self, topic: str, difficulty: str) -> Dict:
        return {
            "task_type": "definition",
            "steps": [
                "Provide clear definition",
                "Add brief context"
            ],
            "prompt_template": f"Define {topic} clearly for a {difficulty} level student."
        }
    
    def _plan_comparison(self, topic: str, difficulty: str) -> Dict:
        return {
            "task_type": "comparison",
            "steps": [
                "Identify items to compare",
                "List similarities",
                "List differences",
                "Provide conclusion"
            ],
            "prompt_template": f"Compare and contrast the concepts in: {topic}. Suitable for {difficulty} level."
        }
    
    def _plan_practice(self, topic: str, difficulty: str) -> Dict:
        return {
            "task_type": "practice",
            "steps": [
                "Generate practice problems",
                "Provide step-by-step solutions"
            ],
            "prompt_template": f"Create {difficulty} level practice exercises for {topic} with solutions."
        }
    
    def _plan_general(self, topic: str, difficulty: str) -> Dict:
        return {
            "task_type": "general",
            "steps": ["Respond to query"],
            "prompt_template": f"Help the student with: {topic}. Respond at a {difficulty} level."
        }
