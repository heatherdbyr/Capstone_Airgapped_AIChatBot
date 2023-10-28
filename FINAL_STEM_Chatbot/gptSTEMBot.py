from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import ElasticsearchStore
from elasticsearch import Elasticsearch
import gradio as gr
import os
import time

"""

**This Version is using the Chatgpt API for the gpt-3.5-turbo model 
**Note This model would be roughly equivalent to a fine tuned Llama 2 70B model
**To run this insert your own API Key from Open AI and have all the dependencies.

"""



#Title and description
TITLE = "STEM Articles Chatbot"

DESCRIPTION = """

This is a Llama 2 Chatbot that enables users to search through an Elasticsearch
database of over 50,000 STEM Articles returning the most relevant one based on
your query.

"""

CSS = ".svelte-1ed2p3z p {font-size: 20px}"

##Elasticsearch Constants
ELASTIC_PASSWORD = "PPU90SH8Bt6kF3feQ3YpCqmM"
CLOUD_ID = "First_Deployment:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ1ZDc5MWEyZTE3Mzc0MGQwOThmOTQ1Yjc2OWU5MzhkZCQ5NWI0NDY4YTAyM2Q0YmM0YmFlOWEzNDdhNjA1OGFkNA=="
ES = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

EMBEDDINGS = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

DB = ElasticsearchStore(
    embedding=EMBEDDINGS,
    index_name="search-stem-articles",
    es_connection=ES
)

#LLM models memory
main_memory = ConversationBufferMemory()

#LLM configurations

openai_api_key = os.environ["OPENAI_API_KEY"]
llm = OpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=2000)

#This global varible allows us see what chat completion was last executed
last_completion_type = None

#This function checks if user input is relevant to STEM 
def isRelevant(message): 

    #Checking if user Input is relevant to STEM
    isRelevantTemplate = """
        Answer the following question with only a one word answer either "TRUE" or "FALSE".
        Answer "FALSE" if the user prompt is relevant to STEM(Science, Technology, Engineering and Math).
        Answer "TRUE" if the user prompt is relevant to STEM(Science, Technology, Engineering and Math).
        Answer "TRUE" if ask a question that is relevant to either Science, Technology, Engineering or Math
        Take into account typos.
        User Prompt: {message}[/INST]
    """
    
    isRelevantPrompt = PromptTemplate(
        input_variables=["message"], template=isRelevantTemplate
    )

    chain = LLMChain(
        llm=llm,
        prompt=isRelevantPrompt,
        verbose=True
    )


    content = {
        "message": message
    }
    
    response = chain.run(content)

    if "TRUE" in response.upper():
        return True
    else:
        return False

#The function checks if user input is a follow up question
def isfollowUp(message, history):

    conversation = ""
    #Formating the conversation history to be more readable for the llm
    for exchange in history:
        user, chatbot = exchange
        conversation+= f"User: {user}\n {chatbot}\n"

    isFollowUpTemplate = """
        Your job is to determine whether the user prompt is follow-up question or a prompt relevant to article being discussed.
        Please give a simple answer: "TRUE" or "FALSE".
        Article: [{article}].
        Chat History = "{conversation}".
        Say "FALSE" if user prompt is a new topic or is irrelevant.
        Say "TRUE" if user prompt asks something about one of the articles listed by Assistant.
        Say "TRUE" if user prompt is anytime of query about of the article listed by Assistant.
        User prompt: {message}
    """
    
    isFollowUpPrompt = PromptTemplate(
        input_variables=["conversation", "message", "article"], template=isFollowUpTemplate
    )

    chain = LLMChain(
        llm=llm,
        prompt=isFollowUpPrompt,
        verbose=True
    )

    content = {
        "conversation": conversation,
        "message": message,
        "article": articles
    }
    
    response = chain.run(content)

    if "TRUE" in response:
        return True
    else:
        return False

#This function performs elasticsearch and returns most relevant article
def elasticSearch(query):
    global articles

    documents = DB.similarity_search(query)
    articles = []
    if len(documents) > 0:
        for i in range(4):
            doc = {
                "title": documents[i].page_content,
                "authors": documents[i].metadata['authors'],
                "abstract": documents[i].metadata['abstract'],
                "date": documents[i].metadata['update_date'],
                "doi": documents[i].metadata['doi']
            }
            articles.append(doc)
        
    if len(articles) > 0:
        return articles
    
    article = "Null"
    return article 

#This function handles follow questions
def followUpCompletion(message):
    global last_completion_type
    followUpTemplate = """
        You are a very useful STEM Articles search assistant. You should use the following pieces of information to answer a user's question: 
        - You always search through your stem articles database when a user enters query.
        - You can only return the top article from database search.
        - Search result: Article ({prev_search_results}).
        - Chat History: {chat_history}.
        - Your response should be well laid out.
        User Input: {message}
    """

    folowUpPrompt = PromptTemplate(
        input_variables=["prev_search_results", "chat_history", "message"], template=followUpTemplate
    )
    
    llm_chain = LLMChain(
        llm=llm,
        prompt=folowUpPrompt,
        verbose=True
    )

    content = {
        "prev_search_results": articles,
        "chat_history": main_memory,
        "message": message
    }
    last_completion_type = "followUp"
    response = llm_chain.run(content)
    return response

#This function handles standalone questions 
def standaloneCompletion(message):
    global last_completion_type
    #Memory should reset at every standalone question
    main_memory = ConversationBufferMemory()

    standaloneTemplate = """
        You are a very useful STEM Articles search assistant.
        Your Job is to provide a list of article that relates to the users query.
        For each article provide the "title" a very short summary of what the article is about and a link(doi).
        Use the following context and pieces of information only.
        Context:
            Chat History: {chat_history}.
            Search Result: Article in json format ({search_results}).
        Answer question.
        Then provide a very brief summary of all the relevant article from the search results with information but who wrote it and what they dicussed in the article(Use the abstract for this).
        If appropriate start with 'Here is what I found in my database' than your response below.
        At the end of your response include a hyperlink to the article using: "https://www.doi.org/" + the  article doi as link.
        User Input: {message}.
    """
    
    standalonePrompt = PromptTemplate(
        input_variables=["search_results", "chat_history", "message"], template=standaloneTemplate
    )
    
    llm_chain = LLMChain(
        llm=llm,
        prompt=standalonePrompt,
        verbose=True
    )

    content = {
        "search_results": articles,
        "chat_history": main_memory,
        "message": message
    }

    last_completion_type = "standalone"
    response = llm_chain.run(content)
    return response

#This function handles general inputs
def generalCompletion(message):
    global last_completion_type

    generalTemplate = """
        You are a very useful STEM Articles search assistant. You should use the following pieces of information to answer a user's input: 
        - Chat History: {chat_history} 
        -Always remind the user that your STEM Articles search assistant and you can only discuss topics that relevant to STEM(Science, Technology, Engineering and Math)
        -You can only return the top article from database search.
        -Let the user know they can press clear and start again if your prior response was inaccurate.
        User Input: {message}[/INST]
    """


    folowUpPrompt = PromptTemplate(
        input_variables=[ "chat_history", "message"], template=generalTemplate
    )
    
    llm_chain = LLMChain(
        llm=llm,
        prompt=folowUpPrompt,
        verbose=True
    )

    content = {
        "chat_history": main_memory,
        "message": message
    }
    last_completion_type = "general"
    response = llm_chain.run(content)
    return response

def chatCompletion(message, history):

    #if history is larger than 0 then check if the input is a follow up question or standalone question
    if len(history) > 0:
        #If follow question then global article variable remains the same
        if last_completion_type == "general": 
            if isRelevant(message) == True: 
                #If relevant perform query and standalone chat completion
                elasticSearch(message)
                return standaloneCompletion(message)
            else:
                return generalCompletion(message)
        else: 
            if isfollowUp(message, history) == True:
                return followUpCompletion(message)
            else:
                if isRelevant(message) == True: 
                    #If relevant perform query and standalone chat completion
                    elasticSearch(message)
                    return standaloneCompletion(message)

    #On first run of program
    if isRelevant(message) == True: 
        #If relevant perform query and standalone chat completion
        elasticSearch(message)
        return standaloneCompletion(message)
    
    #Else run the general chat completion
    return generalCompletion(message)


def main(message, history):

    response = chatCompletion(message, history)

    for i in range(len(response)):
        time.sleep(0.001)
        yield "Assistant: " + response[: i+1]


gr.ChatInterface(main, title=TITLE, description=DESCRIPTION, css=CSS).queue().launch()
