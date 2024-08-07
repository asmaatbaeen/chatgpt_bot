import os
import openai
import asyncio
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi import Request

from threading import Thread
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic import BaseModel

from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_bolt import App

from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from llama_index import SimpleDirectoryReader,GPTVectorStoreIndex
from langchain.memory import ConversationBufferMemory
 
from settings import settings

# Read keys from settings
SLACK_BOT_TOKEN = settings.SLACK_BOT_TOKEN
SLACK_APP_TOKEN = settings.SLACK_APP_TOKEN
OPENAI_API_KEY = settings.OPENAI_API_KEY

# Set the OPENAI_API_KEY environment variable, for future calls
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Set up FastAPI
fast_api_app = FastAPI(
    title="ChatGPTWimt",
    description="Application for querying information about our documents, or redirecting to ChatGPT",
)
fast_api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@fast_api_app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")


@fast_api_app.get("/health")
async def root():
    return {"status": "healthy"}

# Event API & Web API
app = App(token=SLACK_BOT_TOKEN) 
client = WebClient(SLACK_BOT_TOKEN)

# load documents from materials directory
loader = PyPDFDirectoryLoader("materials")
documents = loader.load()

# split the documents into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# # select which embeddings we want to use
embeddings = OpenAIEmbeddings()

# # create the vectorestore to use as the index
db = Chroma.from_documents(texts, embeddings, persist_directory=".")
db.persist()
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":2})
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# # create a chain to answer questions 
qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0.9, model_name="text-davinci-003"), retriever, memory=memory, chain_type='map_reduce')
 
 
# chat api endpoint  
@fast_api_app.post("/wimtgpt")
async def root(request: Request): 
   
    question =  await request.json()
    question = question["query"]
    response = qa({"question": question})
    return response
    



# This gets activated when the bot is tagged in a channel    
@app.event("app_mention")
def handle_message_events(body, logger):
    # Log message
    print(str(body["event"]["text"]).split(">")[1])
    
    # Create prompt for ChatGPT
    prompt = str(body["event"]["text"]).split(">")[1]
    
    # Let the user know that we are busy with the request 
    client.chat_postMessage(channel=body["event"]["channel"], 
        thread_ts=body["event"]["event_ts"],
        text=f"Hello from your bot! :robot_face: \nThanks for your request, I'm on it!")
    
    result=qa({"question": prompt, "chat_history": ""})

    docs_response=result["answer"].lstrip()

    # If we don't get any response from our documents, redirect to ChatGPT
    if docs_response == "I don't know.":
        answer = "Sorry, I don't have the answer, the context that was used to train the bot does not have that information. :disappointed: . I will direct you to OpenAI ChatGPT for a possible answer."
        client.chat_postMessage(channel=body["event"]["channel"], 
                thread_ts=body["event"]["event_ts"],
                text=f"Here you go: \n{answer}")
        
        # Check ChatGPT
        chatgpt_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5).choices[0].text
        
        client.chat_postMessage(channel=body["event"]["channel"], 
            thread_ts=body["event"]["event_ts"],
            text=f"Here you go: \n{chatgpt_response}")

    else:
        # Reply to thread 
        client.chat_postMessage(channel=body["event"]["channel"], 
                thread_ts=body["event"]["event_ts"],
                text=f"Here you go: \n{docs_response}")


@app.message()
def handle_message(message, say):
    user = message['user']
    text = message['test']

    say(f"Hi there, <@{user}>! You said: {text}. If you want to interact, please @me in a channel.")

def launch_fastapi():
    uvicorn.run(fast_api_app, host="0.0.0.0", port=8000)

def launch_slackapp():
    SocketModeHandler(app, SLACK_APP_TOKEN).start()

def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        launch_fastapi,
        trigger="date",
        next_run_time=datetime.now(),
    )
    scheduler.add_job(
        launch_slackapp,
        trigger="date",
        next_run_time=datetime.now(),
    )

    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    main()







