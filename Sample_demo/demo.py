from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from dateutil.parser import parse
import replicate 
import streamlit as st 
import time
import os
import re

# Set the environment variable
os.environ['REPLICATE_API_TOKEN'] = 'r8_X1qWO35dTBKsIN7GQbSrbuWVBu89Onf1c8SGt'
API_URL = "https://ln9afaz9wxel05le.us-east-1.aws.endpoints.huggingface.cloud/"

MODEL_NAME = "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3"

headers = {
	"Authorization": "Bearer TeWAqUDMIdoqDyPtnisCRPddnmdPBhScjqWuIWkQtvyOuPIqBeRtpycLbXBrKFldVGLrTKEjVGIkbHzjBkmqYMoHjjWTgoBzhCBFaeSIACuAdHxvGLBiXgYJVzidmbKY",
	"Content-Type": "application/json"
}

#words can be filtered out of searches to elastic
MISC_WORDS = [
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
    "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's",
    "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself",
    "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of",
    "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves",
    "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's",
    "should", "shouldn't", "so", "some", "such", "tell", "than", "that", "that's",
    "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
    "these", "they", "they'd", "they'll", "they're", "they've", "this", "those",
    "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we",
    "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when",
    "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why",
    "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're",
    "you've", "your", "yours", "yourself", "yourselves", "hi", "hello", "love", "can",
    "about"
]

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

    keywords = [word for word in userInput.split() if word.lower() not in MISC_WORDS]
    subject_query = " ".join(keywords)

    # Attempt to parse the user input as a date
    date_query = None
    try:
        if re.search(r'\d.*\d', userInput):
            parsed_date = parse(userInput, fuzzy=True)
            
            # Check if the parsed date has a year, month, and day
            if parsed_date.year and parsed_date.month and parsed_date.day:
                date_query = {
                    "term": {
                        "date": parsed_date.strftime("%Y-%m-%d")
                    }
                }
    except ValueError:
        # If parsing as a date fails, simply pass
        pass

    # Create a text query
    text_query = {
        "multi_match": {
            "query": subject_query,
            "fields": [
                "headline^3",  # boost headlines
                "short_description^2",  # boost short descriptions
                "authors",
                "category",
                "link"
            ],
            "type": "best_fields",
            "fuzziness": "AUTO"
        }
    }

    # Modify the bool query to use "should" for boosting relevance
    query = {
        "bool": {
            "should": [
                text_query,
                {
                    "match": {
                        "headline": subject_query
                    }
                },
                {
                    "match": {
                        "short_description": subject_query
                    }
                }
            ]
        }
    }

    # Add the date query if it exists
    if date_query:
        if "must" not in query["bool"]:
            query["bool"]["must"] = []
        query["bool"]["must"].append(date_query)

    # Create a search object
    s = Search(using=es, index="search-llama2").query(query)

    # Execute the search
    responses = s.execute()

    response_list = []
    for hit in responses[:10]:
        response = {
            "headline": hit.headline,
            "date": hit.date,
            "link": hit.link,
            "short_description": hit.short_description,
            "category": hit.category
        }

        if hasattr(hit, 'author'):
            response['author'] = hit.author
        elif hasattr(hit, 'authors'):
            response['authors'] = hit.authors
        
        if response['link'].count('http') > 1:
            clean_link = response['link'].split('http')[-1]
            response['link'] = 'http' + clean_link

        response_list.append(response)  

    return response_list if response_list else None
    

def isFollowUp(userInput, history): 

    followUpSys = f"""
        [SYSTEM] Context is key. Please consider:
        [SYSTEM] Previous user input: '{history[-3]}'
        [SYSTEM] Assistant's last response: '{history[-2]}'
        [SYSTEM] Current user input: '{userInput}'
    """
    followUpTemplate = f"""
    Answer with TRUE or FALSE only. Is the current userInput, a follow up question on the same exact topic as the previous user input?
    """

    output = replicate.run(
        MODEL_NAME,
        input={"system_prompt": followUpSys,
            "prompt": followUpTemplate,
        "temperature":0.10,
           "max_new_tokens":128,
           "max_length":128
        }
    )
    response = ''.join(output)
    print(f"Follow up response: {response}")

    if "TRUE" in response:
        return True
    else:
        return False
    

def chatCompletion(userInput, history):
    #use case document
    searchErr = "Sorry I couldn't find any articles related to your query. Please try again."
    response = ""

  #  Check if the conversation has history
    response_list = None
    if len(history) > 2:
        #Check if the user input is a follow up question
        if isFollowUp(userInput, history):
            response_list = st.session_state.prev_response_list
        else:
            response_list = elasticSearch(userInput)
            st.session_state.prev_response_list = response_list
        #if not make a new search
    else:
        response_list = elasticSearch(userInput)
        st.session_state.prev_response_list = response_list


    if response_list is None:
        return searchErr

    # Create a list of article titles and links for a more conversational response
    article_responses = []
    for idx, article in enumerate(response_list, start=1):
        if 'author' in article:
            author_str = f" by {article['author']}"
        elif 'authors' in article:
            author_str = f" by {article['authors']}"
        else:
            author_str = ""

        article_response = f"{idx}. [{article['headline']}](Link: {article['link']}) - Author: {author_str} - {article['short_description']} - {article['date']}"
        article_responses.append(article_response)

    # Join the article responses with line breaks
    article_list = "\n".join(article_responses)
    print(article_list)


    system_prompt = """
        [SYSTEM] If the user initiates a conversation, engage without sending articles. You should be friendly in all responses.
        [SYSTEM] If the user asks a question, respond concisely with relevant article details.
        [SYSTEM] If asked for specific details (date, author, link), provide them.
        [SYSTEM] Avoid echoing the user's input.
        [SYSTEM] Only provide genuine articles; no fakes.
    """


    template = f"""
    [SYSTEM] Conversation history: '{history}'
    [SYSTEM] Latest User Input: '{userInput}'
    [SYSTEM] Articles found:
    {article_list} 
    """

    output = replicate.run(
        MODEL_NAME,
        input={"system_prompt": system_prompt,
            "prompt": template,
               "temperature": 0.20,
               "max_new_tokens": 8000,
               "max_length": 8000,
               "debug": True
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
