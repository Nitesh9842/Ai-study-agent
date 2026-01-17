from datetime import datetime
from typing import Optional


class StateTracker:
    def __init__(self):
        self.conversation_history = []
        self.current_topic = None
        self.difficulty_level = "intermediate"
        self.session_start = datetime.now()
        self.topics_covered = []
    
    def update_state(self, user_input: str, parsed_input: dict, response: str):
        """Update the conversation state with new interaction."""
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "parsed": parsed_input,
            "response": response
        })
        
        if self.current_topic and self.current_topic not in self.topics_covered:
            self.topics_covered.append(self.current_topic)
    
    def set_topic(self, topic: str):
        """Set the current study topic."""
        self.current_topic = topic
    
    def set_difficulty(self, level: str):
        """Set the difficulty level."""
        if level in ["beginner", "intermediate", "advanced"]:
            self.difficulty_level = level
    
    def get_context(self, num_messages: int = 5) -> list:
        """Get recent conversation context."""
        return self.conversation_history[-num_messages:]
    
    def get_session_summary(self) -> dict:
        """Get a summary of the current session."""
        return {
            "session_duration": str(datetime.now() - self.session_start),
            "topics_covered": self.topics_covered,
            "total_interactions": len(self.conversation_history),
            "current_topic": self.current_topic,
            "difficulty_level": self.difficulty_level
        }
    
    def reset(self):
        """Reset the state for a new session."""
        self.conversation_history = []
        self.current_topic = None
        self.difficulty_level = "intermediate"
        self.session_start = datetime.now()
        self.topics_covered = []
