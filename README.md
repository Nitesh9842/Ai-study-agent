# 🎓 AI Study Buddy Agent

An intelligent study assistant powered by Groq's LLM API to help students learn effectively.

## Features

- **Explain** concepts at different difficulty levels
- **Summarize** topics concisely
- **Quiz** generation for self-assessment
- **Define** terms clearly
- **Compare** different concepts
- **Practice** exercises with solutions

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure your API key in `.env`:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

3. Run the application:

   **Command Line Interface:**
   ```bash
   python app.py
   ```

   **Web UI (Streamlit):**
   ```bash
   streamlit run ui.py
   ```

## Web UI Features

- 💬 **Chat Interface** - Interactive conversation with the AI tutor
- 🔍 **Agent Pipeline Viewer** - See how each agent component processes your query
- ⚙️ **Settings Panel** - Adjust difficulty level
- 📊 **Session Stats** - Track your learning progress
- ⚡ **Quick Actions** - One-click prompts for common study tasks

## Agent Components

| Component | Description |
|-----------|-------------|
| 🧠 Input Understanding | Parses user input and classifies intent |
| 📍 State Tracker | Maintains conversation context and session state |
| 📋 Task Planner | Creates execution plans based on intent |
| ✨ Output Generator | Generates responses using LLM |

## Project Structure

```
ai-study-agent/
├── app.py                 # CLI entry point
├── ui.py                  # Streamlit Web UI
├── agent/
│   ├── __init__.py
│   ├── input_understanding.py
│   ├── state_tracker.py
│   ├── task_planner.py
│   └── output_generator.py
├── config.py
├── requirements.txt
└── README.md
```

## Example Queries

- "Explain photosynthesis"
- "Quiz me on World War 2"
- "What is the difference between DNA and RNA?"
- "Define machine learning"
- "Practice problems for calculus derivatives"
