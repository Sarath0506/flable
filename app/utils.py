from typing import List, Dict

def format_research_output(summary: str, sources: List[Dict], followup_questions: List[str]) -> str:
    """Format the research output with sources and follow-up questions"""
    sources_html = ''.join(
        f'<li style="margin-bottom: 10px;">'
        f'<a href="{source["url"]}" target="_blank" style="color: #3498db; text-decoration: none;">'
        f'{source["title"]}</a> - {source.get("domain", "Unknown")}</li>'
        for source in sources[:5]
    )
    
    questions_html = ''.join(
        f'<li style="margin-bottom: 10px; cursor: pointer; color: #3498db;" '
        f'onclick="askQuestion(\'{question}\')">{question}</li>'
        for question in followup_questions
    )
    
    return f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
        <div style="margin-bottom: 20px; white-space: pre-line;">
            {summary}
        </div>
        
        <div style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
            <h3 style="color: #2c3e50;">Sources:</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                {sources_html}
            </ul>
        </div>
        
        <div style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
            <h3 style="color: #2c3e50;">Follow-up Questions:</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                {questions_html}
            </ul>
        </div>
    </div>
    """
