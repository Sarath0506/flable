# Marketing Research Agent

A FastAPI-based web application that performs marketing research using AI, Brave Search, and provides real-time streaming responses.

## Features

- Real-time streaming responses similar to ChatGPT
- Marketing-focused research using Brave Search
- AI-powered summary generation using GPT-4
- Source tracking and citation
- Follow-up question suggestions
- History management with SQLite database
- Clean, responsive UI

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd flable
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Replace `.env.example` file to `.env` in the root directory with your API keys:
    OPENAI_API_KEY=your_openai_api_key
    BRAVE_API_KEY=your_brave_api_key


## Usage

1. Start the server:
```bash
python main.py
```

2. Open your browser and navigate to: http://localhost:8000


3. Enter your marketing research question in the input field and press Enter or click "Ask"

## Features in Detail

### Real-time Streaming
- Responses are streamed in real-time as they're generated
- Progress is visible to users immediately
- Similar experience to ChatGPT

### Research Capabilities
- Uses Brave Search for up-to-date information
- AI-powered summary generation
- Relevant source tracking
- Follow-up question suggestions

### History Management
- All research is saved to SQLite database
- View previous research results
- Delete individual entries
- Clear entire history

### User Interface
- Clean, responsive design
- Three-column layout:
  - Question input
  - Response display
  - History sidebar
- Clickable follow-up questions
- Source links

## API Endpoints

- `GET /` - Home page
- `POST /ask` - Submit a research question
- `GET /history` - Get research history
- `DELETE /history/{entry_id}` - Delete specific history entry
- `DELETE /history/clear` - Clear all history
