
from flask import Flask, render_template,request

#DEVELOPMENT_ENV = True

app = Flask(__name__)


import os
import openai

# OpenAI Credentials...
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
os.environ["OPENAI_API_BASE"] = "https://cstoai-eastus.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "228e404c5ace452880b0c4ed50bf40c5"
deployment_id="gpt-4-32k"

openai.api_type="azure"
openai.api_version = "2023-05-15"
openai.api_base = "https://cstoai-eastus.openai.azure.com/"
openai.api_key="228e404c5ace452880b0c4ed50bf40c5"

# Set the Table and column Name, these are Case Senstitive
table_name="getSwitch"
colname="Cluster,Device,TIMESTAMP,Switch,Title,Severity,Type"

# Function which accepts user prompt and return Kusto Query
def convert_to_kusto(queryText):
    
    if ('summarize' in queryText) or ('Summarize' in queryText):
        queryText = queryText.replace("summarize","give details of")
        queryText = queryText.replace("Summarize","give details of")
        
    
    response = openai.ChatCompletion.create(
    deployment_id=deployment_id,
    messages=[
        {
        "role": "system",
        
"content": f"Given the following kusto table name <<< {table_name} >>> having columns {colname}, your job is to write kusto queries given a user’s request.output should be only kusto query." 
        },
        {
        "role": "user",
        "content": queryText
        }
    ],
    temperature=0,
    max_tokens=1024
    )
    return response["choices"][0]["message"]['content'].replace("\n"," ")

def replace_text(txt):
    return txt.replace("```","").replace("kusto","").strip()

# API definition
@app.route("/GenerateKustoQuery/<userprompt>", methods=['GET', 'POST'])
def GenerateKustoQuery(userprompt):
    print(userprompt)
    generatedquery=convert_to_kusto(userprompt)

    return replace_text(generatedquery)


if __name__ == "__main__":
    app.run()
