from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from dateutil.parser import parse
import replicate 
import streamlit as st 
import time
import os

# Set the environment variable
os.environ['REPLICATE_API_TOKEN'] = 'r8_X1qWO35dTBKsIN7GQbSrbuWVBu89Onf1c8SGt'
API_URL = "https://ln9afaz9wxel05le.us-east-1.aws.endpoints.huggingface.cloud/"
#Note that varibles above are empty. If you want to run this I'll put the keys on discord

MODEL_NAME = "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e"

headers = {
	"Authorization": "Bearer TeWAqUDMIdoqDyPtnisCRPddnmdPBhScjqWuIWkQtvyOuPIqBeRtpycLbXBrKFldVGLrTKEjVGIkbHzjBkmqYMoHjjWTgoBzhCBFaeSIACuAdHxvGLBiXgYJVzidmbKY",
	"Content-Type": "application/json"
}

CURR_DOC = []

def display_chat_history(messages):
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def elasticSearch(userInput):
    ELASTIC_PASSWORD = "xel8PSGj3Bofb8vuR0FQK2NS"

    CLOUD_ID = "Test_Deployment:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ0MzJmODIyY2RmZDI0MWU1ODY5OTFiMGJiZGI1YjgzNyRhNjE0MzU1M2FhM2U0M2NhYjIwOTAyOTdhNWM2N2EyMA=="

    es = Elasticsearch(
        cloud_id=CLOUD_ID,
        basic_auth=("elastic", ELASTIC_PASSWORD)
    )

    try:
        parsed_date = parse(userInput, fuzzy=True)
        if parsed_date.year is None or parsed_date.month is None or parsed_date.day is None:
            raise ValueError("Invalid date")
        # If a date was successfully parsed, create a date-based query
        date_query = {
            "term": {
                "date": parsed_date.strftime("%Y-%m-%d")
            }
        }
    except ValueError:
        # If parsing as a date fails, treat it as a regular text query
        date_query = None

    text_query = {
        "multi_match": {
            "query": userInput,
            "fields": ["authors", "headline", "category", "short_description", "link"],
            "type": "best_fields"
        }
    }

    s = Search(using=es, index="search-llama2")
    if date_query:
        s = s.query(date_query)
    else:
        s = s.query(text_query)
    responses = s.execute()

    response_list = []
    response_counter = 0
    for hit in responses:
        if response_counter >= 10:
            break
        response_counter += 1

        response = {"headline": hit.headline, "date": hit.date, "link": hit.link, "short_description": hit.short_description, "category": hit.category}

        if hasattr(hit, 'author'):
            response['author'] = hit.author
        elif hasattr(hit, 'authors'):
            response['authors'] = hit.authors

        response_list.append(response)

        print("Relevant Article Headline:", hit.headline)
        print("Relevant Article Date:", hit.date)
        print("Relevant Article Link:", hit.link)
        print("Relevant Article Short Description:", hit.short_description)
        print("\n")

    # Check if any results were returned
    if len(response_list) > 0:
        CURR_DOC = response_list
        return CURR_DOC
    else:
        return None
    
def isFollowUp(userInput, history): 

    followUpTemplate = f"""
        Answer Question with only a one word answer either TRUE or FALSE. If you don't know answer with FALSE.
        This history of conversation: '{history}'
        Question: is this user input '{userInput}' a follow up question of their last question or assistant answer(TRUE/FALSE)? 
    """
    output = replicate.run(
        MODEL_NAME,
        input={"prompt": followUpTemplate,
        "temperature":0.75,
           "max_new_tokens":8000,
           "max_length":8000
        }
    )
    response = ''.join(output)

    if "TRUE" in response:
        return True
    else:
        return False
    

def chatCompletion(userInput, history): 
    #use case document
    searchErr = "Sorry I couldn't find any articles related to your query. Please try again."
    response = ""

  #  Check if the conversation has history
    if len(history) > 2:
        #Check if the user input is a follow up question
        if isFollowUp(userInput, history):
            #if so make use case document the current document
            response_list = CURR_DOC
        else:
            #if not make a new search
            response_list = elasticSearch(userInput)
    else:
        response_list = elasticSearch(userInput)

    if response_list is None:
        return searchErr

    # Create a list of article titles and links for a more conversational response
    article_responses = []
    for idx, article in enumerate(response_list, start=1):
        article_response = f"{idx}. [{article['headline']}]({article['link']}) - {article['short_description']} - {article['date']}"
        article_responses.append(article_response)

    # Join the article responses with line breaks
    article_list = "\n".join(article_responses)

    template = f"""
    [SYSTEM] You are a search assistant with access to the HuffPost archives from 2012 to 2022.
    [SYSTEM] This is the history of our conversation so far: '{history}'
    [SYSTEM] Latest User Input: '{userInput}'

    [SYSTEM] Here are some relevant articles related to the latest input:
    {article_list}

    [SYSTEM] Provide the above info to the user, ENSURE you give the links and maybe give a brief description of each article. 
    [SYSTEM] Please start a new line for each new article.
    """

    output = replicate.run(
        MODEL_NAME,
        input={"prompt": template,
            "temperature": 0.75,
            "max_new_tokens": 4096,
            "max_length": 4096
            }
    )

    for item in output:
        response += item

    return response



def main(): 

    st.title('Llama 2 Air-Gapped ChatBot')

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    #Start of Conversation
    if len(st.session_state.messages) == 0:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            init_response = ""
            assistant_intro = "Hi I am your Huffpost AI assistant\n How may I assist you today?"
            for chunk in assistant_intro.split():
                init_response += chunk + " "
                time.sleep(0.09)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(init_response + "▌")
            message_placeholder.markdown(init_response)
        st.session_state.messages.append({"role": "assistant", "content": init_response})
    else:
        display_chat_history(st.session_state.messages)

    if prompt := st.chat_input("Enter query"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            full_response = chatCompletion(prompt, st.session_state.messages)
            
            # Split the response by '\n' to handle line breaks
            response_paragraphs = full_response.split('\n')
            
            # Display each paragraph with a line break
            for paragraph in response_paragraphs:
                st.write(paragraph)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
