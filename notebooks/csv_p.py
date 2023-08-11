from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import pandas as pd
 
import os

os.environ["OPENAI_API_KEY"] =  "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"
df = pd.read_csv('/Users/asmaatbaeen/Desktop/day5/chatgpt_bot/data_csv/reviews_202301.csv', encoding="utf-16")
pd_agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True)
pd_agent.run("Find the best review")