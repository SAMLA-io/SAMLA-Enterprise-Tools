import pandas as pd
from langchain_groq import ChatGroq
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import os
import dotenv
from fastapi import FastAPI
from pydantic import BaseModel

dotenv.load_dotenv()

# Reading a CSV file
csv_file_path = 'ecommerce_product_dataset.csv'
df_csv = pd.read_csv(csv_file_path)

groq_api = os.getenv('GROQ_API_KEY')
llm = ChatGroq(temperature=0, model="llama3-70b-8192", api_key=groq_api)

# Create the CSV agent
agent = create_csv_agent(llm, csv_file_path, verbose=True, allow_dangerous_code=True)

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_data(request: QueryRequest):
    response = agent.invoke(request.query)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)