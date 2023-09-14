from elasticsearch import Elasticsearch
import replicate 
import streamlit as st 
import time
import os

# Set the environment variable
os.environ['REPLICATE_API_TOKEN'] = ''
API_URL = ""
#Note that varibles above are empty. If you want to run this I'll put the keys on discord

MODEL_NAME = "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e"

headers = {
	"Authorization": "Bearer TeWAqUDMIdoqDyPtnisCRPddnmdPBhScjqWuIWkQtvyOuPIqBeRtpycLbXBrKFldVGLrTKEjVGIkbHzjBkmqYMoHjjWTgoBzhCBFaeSIACuAdHxvGLBiXgYJVzidmbKY",
	"Content-Type": "application/json"
}


#Current document
CURR_DOCUMENT = ""


def elasticSearch(userInput):
    ELASTIC_PASSWORD = "PPU90SH8Bt6kF3feQ3YpCqmM"

    CLOUD_ID = "First_Deployment:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ1ZDc5MWEyZTE3Mzc0MGQwOThmOTQ1Yjc2OWU5MzhkZCQ5NWI0NDY4YTAyM2Q0YmM0YmFlOWEzNDdhNjA1OGFkNA=="
    es = Elasticsearch(
        cloud_id=CLOUD_ID,
        basic_auth=("elastic", ELASTIC_PASSWORD)
    )

    # Define the search query
    query = {
        "query": {
            "multi_match": {
                "query": userInput,
                "fields": ["Title", "content.subtitle.sub_title", "content.subtitle.sub_content"],
                "type": "best_fields"
            }
        },
        "size": 1
    }

    # Execute the search
    response = es.search(index="sample_db", body=query)

    global link
    link = response['hits']['hits'][0]['_source']['Link']


    # Check if any results were returned
    if response['hits']['total']['value'] > 0:
        CURR_DOCUMENT = response['hits']['hits'][0]['_source']
        return CURR_DOCUMENT
    else:
        return None


def checkRelevancy(userInput): 

    relevanceTemplate = f"""
        You are helpful Microsoft Outlook Assistant. Answer Question with only one word answer either TRUE or FALSE. 
        Question: is this user input '{userInput}' relevant to microsoft outlook (TRUE/FALSE)? 
    """
    output = replicate.run(
        MODEL_NAME,
        input={"prompt": relevanceTemplate,
        "temperature":0.75,
           "max_new_tokens":10000,
           "max_length":10000
        }
    )
    
    response = ''.join(output)


    print(response)

    if "TRUE" in response:
        return True
    else:
        return False
    
def isFollowUp(userInput, history): 

    followUpTemplate = f"""
        You are helpful Microsoft Outlook Assistant. Answer Question with only a one word answer either TRUE or FALSE. If you don't know answer with FALSE.
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
    if len(history) > 1:
        #Check if input is relavence to mirosoft outlook
        if checkRelevancy(userInput) == True:
            #if so check it is a follow up question
            if isFollowUp(userInput, history):
                #if so make use case document the current document
                document = CURR_DOCUMENT
        else:
            response = irrelevent
            return response 
    else: 
        #Check if input is relavence to mirosoft outlook
        if checkRelevancy() == False: 
            response = irrelevent
            return response 
    

    #Check if Search was unsuccessfull
    if elasticSearch(userInput) is None:
        response = searchErr
        return response 

    template = f"""
        You are helpful Microsoft Outlook Assistant. Answer Question with only the information below. Answer the Question only don't state what you are.
        Answer question very briefly.
        Answer question with the information below.
        This is history of the conversation: '{history}'
        This the article json document: '{document}'
        This is the link to provide at the end of answer: '{link}'
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
            assistant_intro = "Hi I am your Microsoft support AI assistant\n How may I assist you today?"
            for chunk in assistant_intro.split():
                init_response += chunk + " "
                time.sleep(0.09)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(init_response + "▌")
            message_placeholder.markdown(init_response)
        st.session_state.messages.append({"role": "assistant", "content": init_response})


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