# Import FastAPI framework
from fastapi import FastAPI, Request, UploadFile, File

# Import CORS middleware for frontend-backend communication
from fastapi.middleware.cors import CORSMiddleware

# Import StaticFiles to serve CSS, JS, images
from fastapi.staticfiles import StaticFiles

# Import HTML response class
from fastapi.responses import HTMLResponse

# Import Jinja2 template engine
from fastapi.templating import Jinja2Templates

# Import BaseModel for request body validation
from pydantic import BaseModel


# Import custom functions from operations.py
from operations import *

# Import custom LLM function from llm.py
from llm import *


# Create FastAPI app instance
app = FastAPI()


# ===================== CORS =====================

# Add CORS middleware
# This allows frontend applications to access backend APIs
app.add_middleware(

    # Middleware class
    CORSMiddleware,

    # Allow requests from all origins
    allow_origins=["*"],

    # Allow cookies and credentials
    allow_credentials=True,

    # Allow all HTTP methods (GET, POST, etc.)
    allow_methods=["*"],

    # Allow all headers
    allow_headers=["*"],
)


# ===================== STATIC FILES =====================

# Mount static folder
# Used for CSS, JavaScript, images
app.mount(

    # URL path
    "/static",

    # Folder name in project
    StaticFiles(directory="static"),

    # Internal name
    name="static"
)


# ===================== TEMPLATES =====================

# Load Jinja2 templates folder
templates = Jinja2Templates(directory="templates")


# ===================== GLOBAL RETRIEVER =====================

# Global variable to store retriever object
retriver_ = None


# ===================== FRONTEND =====================

# Home route
@app.get("/", response_class=HTMLResponse)

# Async function for homepage
async def home(request: Request):

    # Return index.html page
    return templates.TemplateResponse(

        # Pass request object
        request=request,

        # HTML file name
        name="index.html"
    )


# ===================== CHAT REQUEST =====================

# Define request body model
class ChatRequest(BaseModel):

    # User message field
    message: str


# ===================== PDF UPLOAD =====================

# API to upload PDF
@app.post("/upload-pdf")

# Async upload function
async def upload_pdf(file: UploadFile = File(...)):

    # Access global retriever variable
    global retriver_

    # Open file in write-binary mode
    with open(file.filename, "wb") as f:

        # Read uploaded file content
        content = await file.read()

        # Save content into local file
        f.write(content)

    # Create retriever from uploaded PDF
    retriver_ = main_fun(file.filename)

    # Return success message
    return {
        "message": "PDF uploaded and processed successfully"
    }


# ===================== CHAT API =====================

# Chat endpoint
@app.post("/chat")

# Async chat function
async def chat(req: ChatRequest):

    # Access global retriever
    global retriver_

    # Check whether PDF is uploaded
    if retriver_ is None:

        # Return error message if no PDF
        return {
            "reply": "Please upload a PDF first"
        }

    # Get user message from request body
    user_message = req.message


    # ================= RETRIEVAL =================

    # Retrieve relevant chunks from vector DB
    docs = retriver_.invoke(user_message)


    # ================= CONTEXT =================

    # Empty context string
    context = ""

    # Loop through retrieved documents
    for doc in docs:

        # Append document content to context
        context += doc.page_content + "\n"


    # ================= PROMPT =================

    # Create final prompt for LLM
    prompt = f"""
    Answer the question based on the context below.

    Context:
    {context}

    Question:
    {user_message}
    """


    # ================= LLM =================

    # Send prompt to LLM
    model_final_reply = LLM__(prompt)


    # Return final response
    return {

        # Return user question
        "user": user_message,

        # Return model answer
        "reply": model_final_reply
    }