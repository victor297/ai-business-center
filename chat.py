import requests
import json
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set path to your JSON file
JSON_PATH = "test.json"
def customer_support():
    def get_json_text():
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
        
        # Extract array of product descriptions
        products = data.get('products', [])
        # Extract array of product descriptions with proper formatting
        descriptions = []
        for product in products:
            title = product.get('title', 'No Title')
            price = product.get('price', 'No Price')
            category = product.get('category', 'No Category')
            image = product.get('image', 'No Image')
            description = product.get('description', 'No Description')
            
            descriptions.append(f"{title} ${price} {category} {image} {description}")

        # Concatenate all descriptions into a single string
        text = "\n".join(descriptions)
        return text

    def get_text_chunks(text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        chunks = text_splitter.split_text(text)
        return chunks

    def get_vector_store(text_chunks):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")

    # Define the prompt template correctly
    prompt_template = """
    Answer the question, and make sure to provide all links and prices. Include details using this format:
    display the imageurl \n
    display title and $price in bold
    Don't provide the wrong answer.

    Context:\n {context}\n
    Question: \n{question}\n

    Answer:
    """

    def get_conversational_chain():
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
        return chain

    # Process the JSON file and generate text chunks
    json_text = get_json_text()
    text_chunks = get_text_chunks(json_text)
    get_vector_store(text_chunks)

    # User input processing
    def user_input(user_question):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)
        
        chain = get_conversational_chain()
        response = chain(
            {"input_documents": docs, "question": user_question},
            return_only_outputs=True
        )
        
        return response["output_text"]

    # Streamed response generator
    def response_generator(user_question):
        response = user_input(user_question)
        for word in response.split():
            yield word + " "

    # Handle ordering process
    def handle_ordering():
        if "order_proceed" not in st.session_state:
            st.session_state.order_proceed = False
        if "address_provided" not in st.session_state:
            st.session_state.address_provided = False

        # Ask if the user wants to proceed with the order
        if not st.session_state.order_proceed:
            proceed = st.selectbox("Would you like to proceed with the order?", ("Select an option", "Yes", "No"))
            if proceed == "Yes":
                st.session_state.order_proceed = True
            elif proceed == "No":
                st.write("Order canceled.")
                return

        # Ask for the address if the user wants to proceed
        if st.session_state.order_proceed and not st.session_state.address_provided:
            address = st.text_input("Please enter your address:")
            if st.button("Submit Address"):
                if address:
                    st.session_state.address_provided = True
                    st.session_state.address = address
                    st.write(f"Thank you! Your order was successful. It will be delivered to {address}.")
                else:
                    st.write("Please provide a valid address.")

    # Streamlit app setup
    # st.set_page_config(page_title="UjjwalDeepXIXC", page_icon="logo.png", layout="centered")
    st.header(":violet[Chat]Bot", divider='rainbow', help="This bot is designed by Ujjwal Deep to address all of your questions hehe")
    # st.subheader("Hello! There, How can I help you Today- 👩‍💻")
    st.caption(":violet[what a] :orange[good day] :violet[it is] :violet[today] :blue[ask anything you want to buy]")

    # Process the JSON file automatically
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Technology and Networking are the most powerful weapons"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(prompt))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Handle the ordering process
        handle_ordering()
