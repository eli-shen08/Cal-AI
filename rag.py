from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from vector import retriever
from dotenv import load_dotenv
import os


# Loading Environment Variables
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Calling LLM

model = ChatGroq(
    model_name="llama-3.3-70b-versatile",
)


async def get_rag_response(question:str):

    # while True:
    #     question = input("Ask your question (q to exit): ")
    #     if question.lower() == 'q':
    #         break 

    docs = retriever.invoke(question)
    info = "\n".join([doc.page_content for doc in docs])

    
    template = '''
    You are an expert about Calcutta University who answers questions about the university.

    You will be given some information about Calcutta University to answer questions.

    Your answer must be comprehensive, detailed, and structured with bullet points.
    Synthesize information from all relevant chunks provided below.

    If you don't know the answer, say 'Sorry I seem to have no information about this'.

    Here are some relevant info: {info}

    Here is the question : {question} 

    Answer the question based on the provided info
    '''

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model 
    result = chain.invoke({"info": info, "question": question})
    return result

    # print(f'INFORMATION : \n{info}\n')

    # print(f'LLM : {result}')
    # print('LLM : ')
    # for chunk in chain.stream({"info": info, "question": question}):
    #     print(chunk.content,end="",flush=True)
    # print('\n')