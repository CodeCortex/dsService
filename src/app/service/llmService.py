import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_openai import ChatOpenAI
# from langchain_mistralai.chat_models import ChatMistralAI
from service.Expense import Expense
from langchain_core.utils.function_calling import convert_to_openai_tool
from dotenv import load_dotenv, dotenv_values 
from langchain_groq import ChatGroq



class LLMService:
    def __init__(self):
        load_dotenv()
        self.prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert extraction algorithm. "
                "Only extract relevant information from the text. "
                "If you do not know the value of an attribute asked to extract, "
                "return null for the attribute's value.",
            ),
            ("human", "{text}")
        ]
        )
        self.apiKey = os.getenv('GROQ_API_KEY')
        # self.llm = ChatMistralAI(api_key=self.apiKey, model="mistral-small-latest", temperature=0)
        # print("Mistral model:", self.llm.model)
        self.llm = ChatGroq(
            api_key=self.apiKey,
            model="openai/gpt-oss-20b",
            temperature=0
        )
        print("Secret key === "+ self.apiKey)

        print("Groq model:", self.llm.model_name)
        
        self.runnable = self.prompt | self.llm.with_structured_output(schema=Expense)
    
    def runLLM(self, message):
        return self.runnable.invoke({"text":message})