from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SQLDatabase
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI()
chat_model = ChatOpenAI()

db = SQLDatabase.from_uri("sqlite:///./weights.db")

question = "total rows of animal data i have in my system?"

def get_schema(_):
    return db.get_table_info()

def run_query(query):
    return db.run(query)

model = ChatOpenAI()

from langchain.prompts import ChatPromptTemplate

template = """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:"""

prompt = ChatPromptTemplate.from_template(template)

sql_response = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | model.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
)

res = sql_response.invoke({"question": question})
print(res)

template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}"""
prompt_response = ChatPromptTemplate.from_template(template)

full_chain = (
    RunnablePassthrough.assign(query=sql_response)
    | RunnablePassthrough.assign(
        schema=get_schema,
        response=lambda x: db.run(x["query"]),
    )
    | prompt_response
    | model
)

chain_res = full_chain.invoke({"question": question})
print(chain_res)