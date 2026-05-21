from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenRouter(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model='nvidia/nemotron-3-super-120b-a12b:free',
)