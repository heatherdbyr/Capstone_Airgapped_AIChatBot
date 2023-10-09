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
        return response_list
    else:
        return None


# def checkRelevancy(userInput): 

#     relevanceTemplate = f"""
#         Answer Question with only one word answer either TRUE or FALSE. 
#         Question: is this user input '{userInput}' relavant to microsoft outlook (TRUE/FALSE)? 
#     """
#     output = replicate.run(
#         MODEL_NAME,
#         input={"prompt": relevanceTemplate,
#         "temperature":0.75,
#            "max_new_tokens":10000,
#            "max_length":10000
#         }
#     )
    
#     response = ''.join(output)


#     print(response)

#     if "TRUE" in response:
#         return True
#     else:
#         return False
    
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
    document = ""
    irrelevent = "Unfortunately, I am an Microsoft Outlook assistant \n I can only answer questions or queries that pretain to Microsoft Outlook :("
    searchErr = "Unfortunately, I could not find anything related to your query within our database \n as this is only a sample database and is very small"
    response = ""

    #Check if the conversation has history
    # if len(history) > 1:
    #     #Check if input is relavence to mirosoft outlook
    #     # if checkRelevancy(userInput) == True:
    #         #if so check it is a follow up question
    #         if isFollowUp(userInput, history):
    #             #if so make use case document the current document
    #             response_list = CURR_DOC
    #     # else:
    #     #     response = irrelevent
    #     #     return response 
    # else: 
    #     #Check if input is relavence to mirosoft outlook
    #     # if checkRelevancy() == False: 
    #     #     response = irrelevent
    #     #     return response 
    #     print('history nil')
    

    #Check if Search was unsuccessfull
    response_list = elasticSearch(userInput)
    if response_list is None:
        return searchErr

    template = f"""
        You are a search assistant with access to the Huffpost archives from 2012 to 2022.
        Answer question very briefly.
        Answer question with the information below.
        This is history of the conversation: '{history}'
        Here is a list of all the possible responses to the users question: '{response_list}'
        You must answer the question with at least one of the responses above, and you must send the provided link when mentioning an article.
        Question: '{userInput}'
    """

    output = replicate.run(
        MODEL_NAME,
        input={"prompt": template,
            "temperature":0.75,
            "max_new_tokens":4096,
            "max_length":4096
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
            message_placeholder = st.empty()

            full_response = ""
            assistant_response = chatCompletion(prompt, st.session_state.messages)
            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
