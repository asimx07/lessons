# Wikibuddy/main.py

from fastapi import FastAPI, HTTPException
import logging
from Wikibuddy.agent.conversational_agent import ConversationalAgent
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

agent = ConversationalAgent()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "Service is up and running!"}

@app.post("/chat")
async def chat(query: str):
    try:
        response = agent.process_query(query)
        logging.info(f"Processed query: {query}")
        return {"response": response}
    except Exception as e:
        logging.error(f"Error processing query: {query}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def gradio_chat(message, history):
    response = agent.process_query(message)
    return response

io = gr.ChatInterface(
    fn=gradio_chat,
    chatbot=gr.Chatbot(height=400),
    textbox=gr.Textbox(placeholder="Ask Away! ", container=False, scale=6),
    title="WikiBuddy",
    description="Ask me any question",
    theme="soft",
    examples=["Who is David Beckham?", "Is Bitcoin Dead?", "What club does Christiano Ronaldo play for?"],
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
    analytics_enabled=True,
    fill_height=True
)

app = gr.mount_gradio_app(app, io, path="/gradio")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
