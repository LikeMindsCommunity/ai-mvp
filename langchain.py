import os
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def extract_dart_code(text):
    # Pattern to match code blocks with dart, flutter, or no language specified
    pattern = r"```(?:dart|flutter)?\n(.*?)```"
    matches = re.finditer(pattern, text, re.DOTALL)
    dart_codes = []
    
    for match in matches:
        code = match.group(1).strip()
        # Basic validation to check if it's Dart code
        if any(keyword in code for keyword in ['void main()', 'class', 'import', 'Widget']):
            dart_codes.append(code)
    
    return dart_codes

def save_dart_code(code, index=0):
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Determine the filename
    filename = f'output/flutter_code_{index + 1}.dart'
    
    with open(filename, 'w') as f:
        f.write(code)
    print(f"\nSaved Dart code to: {filename}")

def build_retrieval_qa():
    # Load prompt template
    with open('prompt.txt', 'r') as file:
        prompt_content = file.read()

    # Load documents and create vector store (or load existing)
    index_name = "faiss_index_likeminds_docs"
    
    if os.path.exists(index_name):
        print("Loading existing vector store...")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
        vectorstore = FAISS.load_local(index_name, embeddings, allow_dangerous_deserialization=True)
    else:
        print("Creating new vector store from documents...")
        # Load .md files from the directory and subdirectories
        loader = DirectoryLoader(
            'docs/chat', 
            glob="**/*.md",
            loader_cls=UnstructuredMarkdownLoader,
            show_progress=True,
            use_multithreading=True
        )
        docs = loader.load()

        # Split documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        # Create embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

        # Create FAISS vector store
        vectorstore = FAISS.from_documents(splits, embeddings)
        vectorstore.save_local(index_name)

    # Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Initialize Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro-exp-03-25",  # Use the same model as in the original script
        google_api_key=GOOGLE_API_KEY,
        temperature=0.7,
        convert_system_message_to_human=True  # Often needed for Gemini system prompts
    )

    # Define a custom prompt template incorporating system instructions
    system_template = """You are a helpful integration assistant from LikeMinds, which is a company that makes Chat and Feed SDKs in multiple tech stacks (React, React Native, Flutter, Android, and iOS). You are an expert at preparing solutions and integration guides and runnable code in all our supported SDKs. You have access to our documentation which details how everything is supposed to be done. Do not hallucinate any information, provide clear and concise steps.

{prompt_content}

Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Chat History: {chat_history}
Question: {question}
Answer:"""

    # Fill in the prompt_content placeholder
    system_template = system_template.replace("{prompt_content}", prompt_content)
    
    QA_PROMPT = PromptTemplate(
        template=system_template, 
        input_variables=["context", "chat_history", "question"]
    )

    # Use a memory object
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    # Create the chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT}
    )
    
    return qa_chain

def generate():
    # Build the retrieval QA chain
    qa_chain = build_retrieval_qa()
    
    # List of questions to process
    questions = [
        "How do I integrate LikeMinds Chat SDK in Flutter?",
        "How do I customise the appbar on the chatroom screen?"
    ]
    
    # Process each question
    for question in questions:
        print(f"\n\nQuestion: {question}\n")
        result = qa_chain.invoke({"question": question})
        response_text = result['answer']
        print(response_text)
        
        # Extract and save any Dart code found in the response
        dart_codes = extract_dart_code(response_text)
        if dart_codes:
            print("\n\nFound Flutter/Dart code in the response. Saving to files...")
            for i, code in enumerate(dart_codes):
                save_dart_code(code, i)

if __name__ == "__main__":
    generate() 