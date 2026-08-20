# DocuChatBot

DocuChatBot is an AI-powered document question-answering application that allows users to upload PDF documents and ask questions based on their content. The application extracts information from uploaded documents, performs similarity search using vector embeddings, and generates answers using Google Gemini.

## Project Overview

DocuChatBot is designed to make information retrieval from PDF documents easier and faster. Instead of manually searching through a large document, users can upload the PDF and ask questions in natural language.

## Features

- PDF document upload
- Text extraction from PDF files
- Text chunking
- Text embeddings
- FAISS vector storage
- Similarity-based document search
- AI-generated answers using Google Gemini
- Document summary
- Text-to-Speech for generated answers
- User registration and login
- Responsive web interface

## Technology Stack

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- Flask

### AI and NLP

- Google Gemini
- LangChain
- HuggingFace Embeddings
- Sentence Transformers

### Database and Search

- MySQL
- FAISS

### PDF Processing

- PyPDF

## System Architecture

```text
PDF Upload
    |
Text Extraction
    |
Text Chunking
    |
Generate Embeddings
    |
FAISS Vector Storage
    |
User Question
    |
Similarity Search
    |
Relevant Context
    |
Google Gemini
    |
Generated Answer
    |
Chatbot Interface
    |
User
```

## How It Works

1. The user uploads a PDF document.
2. The application extracts text from the PDF.
3. The extracted text is divided into smaller chunks.
4. Embeddings are generated for the text chunks.
5. The embeddings are stored in FAISS.
6. The user enters a question.
7. The application performs a similarity search.
8. Relevant document content is retrieved.
9. The relevant context is sent to Google Gemini.
10. Gemini generates the answer.
11. The answer is displayed to the user.
12. The Text Reader can read the generated answer aloud.

## Project Structure

```text
DocuChatBot/
|
├── app.py
├── requirements.txt
├── README.md
|
├── templates/
│   ├── index.html
│   ├── login.html
│   └── register.html
|
├── static/
│   ├── style.css
│   └── script.js
|
├── uploads/
|
└── database/
    └── database.sql
```

## Installation

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the Project

```bash
cd DocuChatBot
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## API Key Setup

DocuChatBot uses the Google Gemini API to generate AI-based answers.

### Steps to Get Gemini API Key

1. Open Google AI Studio.
2. Sign in using your Google account.
3. Open the API Key section.
4. Click on "Create API Key".
5. Select or create a Google Cloud project if required.
6. Copy the generated API key.
7. Add the API key to your application configuration.

### Configure the API Key

Example:

```text
GEMINI_API_KEY=your_api_key
```

Do not add your real API key to this README file.

Do not share your API key publicly or upload it to GitHub.

## Environment Variables

For better security, store sensitive information in environment variables.

Example:

```text
GEMINI_API_KEY=your_api_key
```

Add sensitive configuration files to `.gitignore` before pushing the project to GitHub.

Example:

```text
.env
venv/
__pycache__/
uploads/
```

## Database Setup

If MySQL is used in the project:

1. Install MySQL.
2. Start the MySQL server.
3. Create the required database.
4. Import the SQL file from the `database` folder.
5. Configure the database credentials in the Flask application.

## Run the Application

Start the Flask application:

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
http://127.0.0.1:5000/register
http://127.0.0.1:5000/login

```

## How to Use

1. Register a new account.
2. Login to the application.
3. Upload a PDF document.
4. Wait for the document to be processed.
5. Enter a question related to the document.
6. Submit the question.
7. View the generated answer.
8. Use the Text Reader feature if you want the answer to be read aloud.
9. Use the Summary feature to generate a document summary.

## Example Questions

After uploading a document, users can ask questions such as:

```text
What is the main topic of this document?

Explain the important points from this document.

Summarize this document.

What are the objectives mentioned in the document?

Explain this topic in simple language.
```

## Screenshots

Add screenshots of the application here after uploading them to the GitHub repository.

Recommended screenshots:

- Login Page
- Registration Page
- Main Dashboard
- PDF Upload
- Question and Answer Section
- Summary Section
- Text Reader
- Generated Image Section

Example:

```text
screenshots/
├── login.png
├── register.png
├── dashboard.png
├── question-answer.png
└── summary.png
```

## Advantages

- Reduces the time required to search large PDF documents.
- Provides natural-language question answering.
- Uses semantic similarity instead of simple keyword matching.
- Can process information from uploaded documents.
- Provides an easy-to-use web interface.
- Supports text-to-speech for generated answers.

## Limitations

- Answer quality depends on the quality and content of the uploaded document.
- Very large documents may require additional processing time.
- Gemini API access requires an API key.
- Internet connectivity may be required for cloud-based AI services.
- API usage may be subject to service limits and pricing.

## Future Scope

- Multiple PDF and document support
- Voice-based questions
- Multilingual question answering
- Cloud deployment
- Advanced document analytics
- User-specific document storage
- Admin dashboard
- Improved response accuracy
- Support for additional document formats
- Conversation history

## Contributors

This project can be developed and maintained by the project team.

## Author

Sarvesh Kumar

## License

This project is developed for educational and project purposes.