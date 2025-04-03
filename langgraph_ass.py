import os
import re
from typing import TypedDict, List, Optional, Annotated, Literal
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.schema import Document
from langgraph.graph import StateGraph, END

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Define state types for the graph
class GraphState(TypedDict):
    question: str
    chat_history: List
    retrieved_docs: List[Document]
    code_generated: Optional[str]
    validation_result: Optional[str]
    final_response: Optional[str]
    error: Optional[str]

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

def get_vectorstore():
    """Get or create the vectorstore"""
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
    
    return vectorstore

# Define nodes for the graph workflow
def retrieve_docs(state: GraphState) -> GraphState:
    """Retrieve relevant documents based on the question"""
    try:
        vectorstore = get_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        docs = retriever.invoke(state["question"])
        return {"retrieved_docs": docs}
    except Exception as e:
        return {"error": f"Error in document retrieval: {str(e)}"}

def generate_code(state: GraphState) -> GraphState:
    """Generate code based on the question and retrieved documents"""
    try:
        # Load prompt template
        with open('prompt.txt', 'r') as file:
            prompt_content = file.read()
        
        # Initialize Gemini model
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro-exp-03-25",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        # Format documents for context
        doc_strings = []
        for doc in state["retrieved_docs"]:
            doc_strings.append(f"Source: {doc.metadata.get('source', 'Unknown')}\nContent: {doc.page_content}")
        
        context = "\n\n".join(doc_strings)
        
        # Create chat history format
        chat_history_str = ""
        if state["chat_history"]:
            for i, msg in enumerate(state["chat_history"]):
                role = "User" if i % 2 == 0 else "Assistant"
                chat_history_str += f"{role}: {msg}\n"
        
        # Define a custom prompt template
        system_template = f"""You are a helpful integration assistant from LikeMinds, which is a company that makes Chat and Feed SDKs in multiple tech stacks (React, React Native, Flutter, Android, and iOS). You are an expert at preparing solutions and integration guides and runnable code in all our supported SDKs. You have access to our documentation which details how everything is supposed to be done. Do not hallucinate any information, provide clear and concise steps.

{prompt_content}

Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Chat History:
{chat_history_str}

Question: {state["question"]}

Answer with explanation and include runnable code examples:"""
        
        # Generate response
        response = llm.invoke(system_template)
        
        # Update the response and extract code
        dart_codes = extract_dart_code(response.content)
        code_generated = dart_codes[0] if dart_codes else None
        
        return {
            "final_response": response.content,
            "code_generated": code_generated
        }
    except Exception as e:
        return {"error": f"Error in code generation: {str(e)}"}

def validate_code(state: GraphState) -> GraphState:
    """Validate the generated code"""
    # For simplicity, we'll do basic validation
    # In a real implementation, this could be more sophisticated
    
    if not state.get("code_generated"):
        return {"validation_result": "no_code"}
    
    code = state["code_generated"]
    
    # Basic checks
    error_indicators = [
        "TODO", "FIXME", "NOT_IMPLEMENTED", 
        "throws UnimplementedError", 
        "// This is just a placeholder"
    ]
    
    for indicator in error_indicators:
        if indicator in code:
            return {"validation_result": "invalid"}
    
    # Check for basic Dart/Flutter syntax
    if not any(keyword in code for keyword in ['class', 'import', 'Widget', 'build']):
        return {"validation_result": "possibly_invalid"}
    
    return {"validation_result": "valid"}

def finalize_response(state: GraphState) -> GraphState:
    """Format the final response and save any code"""
    if state.get("error"):
        return {"final_response": f"An error occurred: {state['error']}"}
    
    if state.get("code_generated") and state.get("validation_result") == "valid":
        # Save the code
        save_dart_code(state["code_generated"])
        
        return {
            "final_response": (
                f"{state['final_response']}\n\n"
                f"Code validation: PASSED\n"
                f"The code has been saved to output/flutter_code_1.dart"
            )
        }
    elif state.get("validation_result") == "no_code":
        return {
            "final_response": (
                f"{state['final_response']}\n\n"
                f"Note: No Flutter/Dart code was found in the response."
            )
        }
    else:
        return {
            "final_response": (
                f"{state['final_response']}\n\n"
                f"Code validation: {state.get('validation_result', 'NOT PERFORMED')}\n"
                f"The code may need review before use."
            )
        }

def should_retry(state: GraphState) -> Literal["regenerate", "finalize"]:
    """Determine if we should retry code generation"""
    validation = state.get("validation_result")
    
    if validation in ["invalid", "possibly_invalid"]:
        return "regenerate"
    else:
        return "finalize"

def build_workflow():
    # Define the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("retriever", retrieve_docs)
    workflow.add_node("generator", generate_code)
    workflow.add_node("validator", validate_code)
    workflow.add_node("finalizer", finalize_response)
    
    # Define the edges
    workflow.set_entry_point("retriever")
    workflow.add_edge("retriever", "generator")
    workflow.add_edge("generator", "validator")
    
    # Add conditional edges from validator
    workflow.add_conditional_edges(
        "validator",
        should_retry,
        {
            "regenerate": "generator",
            "finalize": "finalizer"
        }
    )
    
    workflow.add_edge("finalizer", END)
    
    # Compile the graph
    return workflow.compile()

def generate():
    # Build the workflow
    app = build_workflow()
    
    # List of questions to process
    questions = [
        "How do I integrate LikeMinds Chat SDK in Flutter?",
        "How do I customise the appbar on the chatroom screen?"
    ]
    
    # Process each question
    chat_history = []
    for question in questions:
        print(f"\n\nQuestion: {question}\n")
        
        # Set initial state
        initial_state = {
            "question": question,
            "chat_history": chat_history,
            "retrieved_docs": [],
            "code_generated": None,
            "validation_result": None,
            "final_response": None,
            "error": None
        }
        
        # Run the workflow
        result = app.invoke(initial_state)
        
        # Print the result
        print(result["final_response"])
        
        # Update chat history for next question
        chat_history.append(question)
        chat_history.append(result["final_response"])

if __name__ == "__main__":
    generate() 