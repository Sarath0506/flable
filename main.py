from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.research_agent import ResearchAgent
from app.sqlite_memory import DatabaseHandler
from app.utils import format_research_output
import os
import json

os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


db = DatabaseHandler()

research_agent = ResearchAgent()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    history = db.view_history()
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "history": history}
    )

@app.post("/ask")
async def ask_question(question: str = Form(...)):
   
    research_results = research_agent.research(question)
    
    formatted_response = format_research_output(
        research_results['summary'],
        research_results['sources'],
        research_results['followup_questions']
    )

    response_data = {
        'summary': research_results['summary'],
        'sources': research_results['sources'],
        'followup_questions': research_results['followup_questions']
    }

    db.save_research(question, json.dumps(response_data))
    
    return {
        "response": formatted_response,
        "sources": research_results['sources'][:5],
        "followup_questions": research_results['followup_questions']
    }

@app.get("/history")
async def get_history():
    history = db.view_history()
    formatted_history = []
    for item in history:
        try:
            
            if isinstance(item[2], str):
                try:
                    response_data = json.loads(item[2])
                except json.JSONDecodeError:
                    
                    response_data = {
                        'summary': item[2],
                        'sources': [],
                        'followup_questions': []
                    }
            else:
                response_data = item[2]
            
            formatted_history.append((
                item[0],  
                item[1],  
                format_research_output(
                    response_data.get('summary', ''),
                    response_data.get('sources', []),
                    response_data.get('followup_questions', [])
                ),
                item[3]   
            ))
        except Exception as e:
           
            formatted_history.append((
                item[0],
                item[1],
                format_research_output(
                    str(item[2]),
                    [],
                    []
                ),
                item[3]
            ))
    
    return {"history": formatted_history}

@app.delete("/history/{entry_id}")
async def delete_history(entry_id: int):
    success = db.delete_entry(entry_id)
    return {"success": success}

@app.delete("/history/clear")
async def clear_all_history():
    try:
        db.cursor.execute('DELETE FROM research_history')
        db.conn.commit()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

import uvicorn

if __name__ == "__main__":
    print('Starting the application. Navigate to http://localhost:8000')
    uvicorn.run(app, host="0.0.0.0", port=8000)

    
