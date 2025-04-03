import os
import re
from typing import Dict, List, Any, TypedDict
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import operator

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Define paths
DOCS_PATH = 'docs/chat'
SDK_SOURCE_PATH = 'code/lib'  # Update this to your actual SDK source path

# Define the state schema for our graph
class GraphState(TypedDict):
    messages: List[Any]  # List of messages exchanged
    question: str        # Current user question
    context: List[str]   # Retrieved document chunks
    response: str        # Current response

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

def get_or_create_vectorstore():
    """Get or create the vector store for document retrieval"""
    index_name = "faiss_index_likeminds_docs"
    
    if os.path.exists(index_name):
        print("Loading existing vector store...")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
        vectorstore = FAISS.load_local(index_name, embeddings, allow_dangerous_deserialization=True)
    else:
        print("Creating new vector store from documents and source code...")
        
        # --- Load Documentation ---
        print("Loading documentation files...")
        docs_loader = DirectoryLoader(
            DOCS_PATH, 
            glob="**/*.md",
            loader_cls=TextLoader,
            show_progress=True,
            use_multithreading=True
        )
        markdown_docs = docs_loader.load()
        
        # --- Load Source Code ---
        print("Loading source code files...")
        if os.path.exists(SDK_SOURCE_PATH):
            code_loader = DirectoryLoader(
                SDK_SOURCE_PATH,
                glob="**/*.dart",  # Load only .dart files
                loader_cls=TextLoader,
                show_progress=True,
                use_multithreading=True
            )
            code_docs = code_loader.load()
            print(f"Loaded {len(code_docs)} Dart source files")
            
            # --- Combine ---
            all_docs = markdown_docs + code_docs
            print(f"Combined {len(markdown_docs)} documentation files and {len(code_docs)} code files")
        else:
            print(f"Warning: SDK source path '{SDK_SOURCE_PATH}' not found. Proceeding with documentation only.")
            all_docs = markdown_docs

        # --- Split Documents ---
        # For code files, we use different splitting parameters
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Smaller chunk size for code
            chunk_overlap=150,
            separators=["\n\n", "\n", " ", ""]  # Default separators
        )
        splits = text_splitter.split_documents(all_docs)
        print(f"Split documents into {len(splits)} chunks")

        # Create embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

        # Create FAISS vector store
        vectorstore = FAISS.from_documents(splits, embeddings)
        vectorstore.save_local(index_name)
        print(f"Vector store created and saved to {index_name}")
    
    return vectorstore

def build_rag_workflow():
    """Build the RAG workflow using LangGraph"""
    # Load prompt template
    with open('prompt.txt', 'r') as file:
        prompt_content = file.read()

    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro-exp-03-25",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.7,
        convert_system_message_to_human=True
    )

    # Get the vector store and create retriever
    vectorstore = get_or_create_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 7})  # Increased to get more context

    # Define the retrieval node
    def retrieve_documents(state: GraphState) -> Dict:
        """Retrieve documents based on the user's question"""
        question = state["question"]
        docs = retriever.invoke(question)
        
        # Extract text from documents
        context = []
        for doc in docs:
            # Add source information to help identify if it's code or documentation
            source = doc.metadata.get('source', 'Unknown source')
            # Check if it's a code file (has .dart extension)
            is_code = source.endswith('.dart')
            
            if is_code:
                # For code files, add a header indicating it's source code
                context.append(f"SOURCE CODE ({os.path.basename(source)}):\n{doc.page_content}")
            else:
                # For documentation, add a header indicating it's documentation
                context.append(f"DOCUMENTATION ({os.path.basename(source)}):\n{doc.page_content}")
                
        return {"context": context}

    # Define the generation node
    def generate_response(state: GraphState) -> Dict:
        """Generate a response using retrieved context and chat history"""
        # Create the prompt with chat history
        system_template = """You are a helpful integration assistant from LikeMinds, which is a company that makes Chat and Feed SDKs in multiple tech stacks (React, React Native, Flutter, Android, and iOS). You are an expert at preparing solutions and integration guides and runnable code in all our supported SDKs. You have access to our documentation and source code which details how everything is supposed to be done. Do not hallucinate any information, provide clear and concise steps.

{prompt_content}

Use the following pieces of context to answer the user's question. The context includes both documentation and source code snippets from the SDK. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}
"""
        
        # Create the prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            MessagesPlaceholder(variable_name="messages"),
        ])
        
        # Prepare the context string
        context_str = "\n\n".join(state["context"])
        
        # Generate the response
        chain = prompt | llm
        response = chain.invoke({
            "context": context_str,
            "prompt_content": prompt_content,
            "messages": state["messages"]
        })
        
        return {"response": response.content}

    # Define the node to process response and extract code
    def process_response(state: GraphState) -> Dict:
        """Process the response and extract any code"""
        response = state["response"]
        
        # Extract and save code
        dart_codes = extract_dart_code(response)
        if dart_codes:
            print("\nFound Flutter/Dart code in the response. Saving to files...")
            for i, code in enumerate(dart_codes):
                save_dart_code(code, i)
        
        # Add the assistant's message to the chat history
        messages = state["messages"].copy()
        messages.append(AIMessage(content=response))
        
        return {"messages": messages}

    # Define the state graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("generate", generate_response)
    workflow.add_node("process", process_response)
    
    # Define the edges
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", "process")
    workflow.add_edge("process", END)
    
    # Compile the graph
    return workflow.compile()

def generate():
    """Run the RAG system using LangGraph with memory"""
    # Build the workflow
    graph = build_rag_workflow()
    
    # Questions to process
    questions = [
        "How do I customise the user tile on participant screen?"
    ]
    
    # Maintain chat history across questions
    messages = []
    
    # Process each question
    for question in questions:
        print(f"\n\nQuestion: {question}\n")
        
        # Update the state with the user's question
        messages.append(HumanMessage(content=question))
        
        # Run the graph
        result = graph.invoke({
            "messages": messages.copy(),
            "question": question,
            "context": [],
            "response": ""
        })
        
        # Print the response
        print(result["response"])
        
        # Update the chat history for the next question
        messages = result["messages"]

if __name__ == "__main__":
    generate() 