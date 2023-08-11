import os
import pickle

from google.auth.transport.requests import Request

from google_auth_oauthlib.flow import InstalledAppFlow
from llama_index import GPTSimpleVectorIndex, download_loader

import flask
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import json
import joblib
import numpy as np
import pandas as pd
import os
import flask
from flask import redirect, url_for, flash
# from flask_restplus import reqparse

import requests
import string
import numpy as np
import pickle as p
import json
import joblib
import shared
from shared import VERSION,max_input_size,num_output,max_chunk_overlap
from scripts import authorize_gdocs
from flask import Flask, render_template, request, url_for, jsonify
from google_auth_oauthlib.flow import InstalledAppFlow
from llama_index import GPTSimpleVectorIndex, download_loader
from llama_index import ServiceContext
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper
from langchain import OpenAI
from llama_index import ServiceContext
from flask import jsonify
from shared import openai_key

app = flask.Flask(__name__)
app.config["DEBUG"] = True
print("chatgbt " + str(VERSION))

 
import os

CORS(app)
os.environ['OPENAI_API_KEY'] = openai_key
app = Flask(__name__)
 
@app.route('/chatgbtai', methods=['POST'])
def chatgbt():
    print("------------------")
     
    dictt = {}
    request_data = request.get_json(force=True)
    query = request_data.get("query")
     
    # This example uses text-davinci-003 by default; feel free to change if desired
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))

    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

    # Load documents from the 'data' directory
    documents = SimpleDirectoryReader('data_doc').load_data()
    index = GPTSimpleVectorIndex.from_documents(
        documents
    )
    # print(query)
    
    for qu in query:
        response = index.query(qu)
        dictt[qu] =  response
        print(response)
        
    return dictt
if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port="5001")
