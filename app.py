from agent import InputUnderstanding, StateTracker, TaskPlanner, OutputGenerator


class StudyBuddyAgent:
    def __init__(self):
        self.input_handler = InputUnderstanding()
        self.state = StateTracker()
        self.planner = TaskPlanner()
        self.generator = OutputGenerator()
    
    def process_query(self, user_input: str) -> str:
        """Process a user query and generate a response."""
        # Step 1: Understand input
        parsed = self.input_handler.parse_input(user_input)
        intent = self.input_handler.classify_intent(user_input)
        
        # Step 2: Update state
        self.state.set_topic(user_input)
        
        # Step 3: Create plan
        plan = self.planner.create_plan(
            intent=intent,
            topic=user_input,
            difficulty=self.state.difficulty_level
        )
        
        # Step 4: Generate response
        context = self.state.get_context()
        response = self.generator.generate_response(plan, context)
        formatted = self.generator.format_response(response, plan["task_type"])
        
        # Step 5: Update state with response
        self.state.update_state(user_input, parsed, response)
        
        return formatted
    
    def set_difficulty(self, level: str):
        """Set the difficulty level."""
        self.state.set_difficulty(level)
        return f"Difficulty set to: {level}"
    
    def get_session_info(self) -> dict:
        """Get current session information."""
        return self.state.get_session_summary()


def main():
    print("🎓 AI Study Buddy Agent")
    print("=" * 40)
    print("Commands: 'quit' to exit, 'difficulty <level>' to change level")
    print("Difficulty levels: beginner, intermediate, advanced")
    print("=" * 40 + "\n")
    
    agent = StudyBuddyAgent()
    
    while True:
        try:
            user_input = input("\n📝 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "quit":
                print("\n📊 Session Summary:")
                print(agent.get_session_info())
                print("\n👋 Goodbye! Happy studying!")
                break
            
            if user_input.lower().startswith("difficulty "):
                level = user_input.split(" ", 1)[1].lower()
                print(agent.set_difficulty(level))
                continue
            
            response = agent.process_query(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
