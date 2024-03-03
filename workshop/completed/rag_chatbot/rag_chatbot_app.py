import streamlit as st #all streamlit commands will be available through the "st" alias
import rag_chatbot_lib as glib #reference to local lib script
 
def reddit_style():
    st.markdown(
        """
        <style>
        /* Main page layout */
        .main {
            background-color: #FFFFFF; /* Black background */
        }

        /* Chat messages */
        .stChatMessage {
            background-color: #FFFFFF; /* Dark grey for chat messages */
            border-radius: 10px;
            border: 1px solid #FF4500; /* Reddit's orangered color */
            margin-bottom: 10px;
            padding: 10px;
            color: #FFFFFF; /* White text */
        }

        /* User chat message */
        .stChatMessage[data-role="user"] {
            background-color: #FF4500; /* Reddit's orangered color */
            color: #FFFFFF; /* White text */
        }

        /* Assistant chat message */
        .stChatMessage[data-role="assistant"] {
            background-color: #4F4F4F; /* Slightly lighter grey */
            color: #FFD700; /* Gold text */
        }

        /* Chat input box */
        .stTextInput>div>div>input {
            border-radius: 20px;
            border: 2px solid #FF4500; /* Reddit's orangered color */
            background-color: #2F2F2F; /* Dark grey */
            color: #FFFFFF; /* White text */
        }

        /* Column */
        .leftC {
            color: #00000;
        }

        /* Page title */
        h1 {
            color: #FF4500; /* Reddit's orangered color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="UBC Reddit Chatbot") #HTML title
st.title("UBC Reddit Chatbot") #page title

with st.container():
    reddit_style()
    st.markdown(
        
    )
    st.title("Title")
    input_text = st.text_area("Write title here", height = 1) #display a chat input box
    st.title("Description") 
    input_text2 = st.text_area("Chat with your bot here", height = 5) #display a chat input box
    go_button = st.button("Go", type="primary") #display a primary button



# with st.container():
#     st.write("---")
#     left_c, mid_c, right_c = st.columns([5,5,5])
#     with left_c:
#         st.header("AHHH")
#         st.write("left")
#     with mid_c:
#         st.header("ooooooooooooooooooooooooooooooooo")
#         st.write("mid")
#     with right_c:
#         st.header("ooooh")
#         st.write("mid")


if 'memory' not in st.session_state: #see if the memory hasn't been created yet
    st.session_state.memory = glib.get_memory() #initialize the memory

if 'chat_history' not in st.session_state: #see if the chat history hasn't been created yet
    st.session_state.chat_history = [] #initialize the chat history

if 'vector_index' not in st.session_state: #see if the vector index hasn't been created yet
    with st.spinner("Indexing document..."): #show a spinner while the code in this with block runs
        st.session_state.vector_index = glib.get_index() #retrieve the index through the supporting library and store in the app's session cache




#Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history: #loop through the chat history
    with st.chat_message(message["role"]): #renders a chat line for the given role, containing everything in the with block
        st.markdown(message["text"]) #display the chat content



#input_text = st.chat_input("Chat with your bot here") #display a chat input box

if go_button: #run the code in this if block after the user submits a chat message
    
    with st.chat_message("user"): #display a user chat message
        st.markdown(str(input_text) + str(input_text2)) #renders the user's latest message
    
    st.session_state.chat_history.append({"role":"user", "text": str(input_text) + str(input_text2)}) #append the user's latest message to the chat history
    
    chat_response = glib.get_rag_chat_response(input_text=input_text, memory=st.session_state.memory, index=st.session_state.vector_index,) #call the model through the supporting library
    
    with st.chat_message("assistant"): #display a bot chat message
        st.markdown(chat_response) #display bot's latest response
    
    st.session_state.chat_history.append({"role":"assistant", "text":chat_response}) #append the bot's latest message to the chat history
    
