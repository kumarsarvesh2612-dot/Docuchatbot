#Flask Application Setup
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
load_dotenv()
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from google import genai
from google.genai import types
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash
from flask import ( Flask, render_template,request,session,redirect,url_for)


user_api_key= os.getenv("GOOGLE_API_KEY")
app = Flask(__name__)
def get_db_connection():
    try:
        port = os.getenv("MYSQL_PORT") or os.getenv("MYSQLPORT") or "3306"
        port = int(port) if str(port).strip() != "" else 3306
        
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST") or os.getenv("MYSQLHOST"),
            port=port,
            user=os.getenv("MYSQL_USER") or os.getenv("MYSQLUSER"),
            password=os.getenv("MYSQL_PASSWORD") or os.getenv("MYSQL_ROOT_PASSWORD") or os.getenv("MYSQLPASSWORD"),
            database=os.getenv("MYSQL_DATABASE") or os.getenv("MYSQLDATABASE")
        )
        return conn
    except Exception as e:
        print(f"Feedback error: {e}")
        return None
app.secret_key="mysecret123"
answer=""
summary=""
image_output=""

UPLOAD_FOLDER ='uploads/'
app.config['UPLOAD_FOLDER']='uploads/'
if not os.path.exists(UPLOAD_FOLDER):
  os.makedirs(UPLOAD_FOLDER)

vectorstore =None
chat_history = []

#Extract PDF text
def get_pdf_text(file_paths):
      text = ""
      for file_path in file_paths:
           reader = PdfReader(file_path)
           for page in reader.pages:
             page_text = page.extract_text()
             if page_text:
                text += page_text+"/n"
      print("Extracted Text Length :",len(text))
      print("Text Preview",text[:500])
      return text

#Text chunking
def get_chunks (text):
      splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
      return splitter.split_text(text)

#Embeding Generation and Vector Store
def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings( model_name="sentence-transformers/all-MiniLM-L6-v2",model_kwargs={'device': 'cpu'})
    print("MODEL USED: all-MiniLM-L6-v2")
    return FAISS.from_texts(chunks, embedding=embeddings)
#Ask question
def ask_question(question):
     global vectorstore,chat_history
     if not vectorstore:
         return "please upload PDF"
     api_key = session.get("api_key") or os.getenv("GOOGLE_API_KEY")
     docs = vectorstore.similarity_search(question,k=8)
     print("Number of Docs:",len(docs))
     context ="\n".join([doc.page_content for doc in docs])
     print("CONTEXT LENGTH:",len(context))
     print("CONTEXT PREVIEW:",context[:1000])
     #Gemini Response Generation

     llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=api_key)

     prompt = f"""
     Your are a helpful AI assistant.
     Answer the user's question using the provided document context:
     
     Document context:
     {context}

      User Question:
     {question}

     if the answer is clearly present in the Document Context, answer it directly.
     Only say "Information not found in document" if the answer is genuinely not present in the 
     document" if the answer is genuinely not present in the Document Context.
     """
     response = llm.invoke(prompt)
     chat_history.append({"q":question,"a":response.content})
     return response.content

#Summarize
def summarize_text():
     global vectorstore
     if not vectorstore:
         return "please upload PDF"
     
     api_key =session.get("api_key") or os.getenv("GOOGLE_API_KEY")
     docs = vectorstore.similarity_search("Summarize this document",k=8)

     llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=api_key)
     context = "\n".join([doc.page_content for doc in docs])
     prompt = f"Summarize the following document in 5 bullet points: \n {context}"
     response = llm.invoke(prompt)

     return response.content

#Image Generation
def generate_image(prompt):
     api_key =session.get("api_key") or os.getenv("GOOGLE_API_KEY")
     if not api_key:
         return "upload api key first"
     try:
         client=genai.Client(api_key=api_key)
         response=client.models.generate_content(model="gemini-2.5-flash-image",contents=prompt,config=types.GenerateContentConfig(response_modalities=["IMAGE"]))
         for part in response.candidates[0].content.parts:
             if part.inline_data:
                 image_data= part.inline_data.data
                 os.makedirs("static/generated",exist_ok=True)
                 image_path="static/generated/generated.png"
                 with open(image_path,"wb") as f:
                     f.write(image_data)
                     return "/static/generated/generated.png"
                 return"image could not be generated."
     except Exception as e:
         print("IMAGE ERROR:",str(e))
         return "Image generation error:" + str(e)
  #PDF Upload and Processing   
#Route
@app.route("/",methods=["GET","POST"])
def index():
     global  answer, summary, image_output
     global vectorstore

     
     if request.method=="POST":
         action= request.form.get("action")
         print("ACTION RECEIVED:",action)
         api_key= request.form.get("api_key")

         if api_key:
             session["api_key"]= api_key

         if action == "save_api":
             if session.get("api_key"):
                 answer="API Key saved successfully"
             else:
                 answer="Please enter API Key."

         elif action == "upload":
             files=request.files.getlist("files")
             if not files:
                 answer="Please select PDF"
             else:
                 file_paths =[]
                 for file in files:
                     if file in files:
                         if file and file.filename:
                             filename=secure_filename(file.filename)
                             file_path=os.path.join(app.config["UPLOAD_FOLDER"],filename)
                             file.save(file_path)
                             file_paths.append(file_path)
                         if file_paths:
                             text=get_pdf_text(file_paths)
                             if not text or not text.strip():
                               answer="Text could not be extracted from PDF."
                             else:
                               chunks=get_chunks(text)
                               vectorstore=create_vector_store(chunks)
                               answer=("PDF uploaded and processed successfully")
                         else:
                             answer=("Text could not be extracted from PDF")


         elif action == "ask":
             question= request.form.get("question","").strip()
             print("Question",question)
             print("VECTORSTORE",vectorstore is not None)
             api_key =(session.get("api_key") or os.getenv("GOOGLE_API_KEY"))
             print("API key available",bool(api_key))
             if not api_key:
                 answer="please enter API key first"
             elif vectorstore is None:
                 answer="Please upload PDF first."
             elif not question:
                 answer = "Please write a question"
             else:
                try:
                
                     answer=ask_question(question)
                     print("ANSWER",answer)
                except Exception as e:
                    print("ASK ERROR",str(e))
                    answer ="Error while answering:" + str(e)
         
         elif action =="summarize":
             api_key=(session.get("api_key") or os.getenv("GOOGLE_API_KEY"))
             if not api_key:
                 summary="Please enter API key First"
             elif vectorstore is None:
                 summary ="Please upload PDF first"
             else:
                 summary=summarize_text()

         elif action == "generate":
             prompt = request.form.get("image_prompt")
             if not prompt:
                 image_output="Please write image prompt"
             else:
                 image_output=generate_image(prompt)
         
        #Displaying the Answer
     return render_template("index.html",answer = answer,summary =summary,image =image_output)

@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html",name=session["user_name"])

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name= request.form["name"]
        email= request.form["email"]
        password= request.form["password"]
        confirm_password= request.form["confirm_password"]
        if password != confirm_password:
          return "Password don't match"
        hashed_password= generate_password_hash(password)
        try:
           con=get_db_connection()
           cursor=con.cursor()
           cursor.execute(
                 """
                 INSERT INTO users(name,email,password)
                 VALUES(%s, %s, %s)
                 """,
                 (name,email,hashed_password))
           con.commit()
           cursor.close()
           con.close()
           return redirect(url_for("login"))
        except mysql.connector.IntegrityError:
             return "Email already registered"
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    email_error=None
    password_error=None
    if request.method=="POST":
        email= request.form["email"]
        password=request.form["password"]
        con = get_db_connection()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            "SELECT*FROM users WHERE email = %s",(email,))
        user = cursor.fetchone()
        cursor.close()
        con.close()
        #Email check
        if not user:
            email_error="Invalid email"
            return render_template("login.html",email_error=email_error)
        #password check
        if not  check_password_hash(user["password"],password):
            password_error="Invalid password"
            return render_template("login.html",password_error=password_error)
        #login successful
        session["user_id"]= user["id"]
        session["user_name"]=user["name"]
        return redirect(url_for("index"))
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/feedback", methods=["GET","POST"])
def feedback():
    if request.method == "POST":
        feedback_text=request.form.get("feedback").strip()
        username = session.get("username","Guest")
        if not feedback_text:
            return render_template("feedback.html",error="Please enter your feedback")
        try:
            conn =get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
            "INSERT INTO feedback(username,feedback)VALUES(%s,%s)",(username , feedback_text))
            conn.commit()
            cursor.close()
            return render_template("feedback.html",success="thank you for your feedback")
        except Exception as e:
            print("Feedback error:",e)
            return render_template("feedback.html",error="Feedback could not be saved.")
    return render_template("feedback.html")
if __name__=="__main__":
     app.run(
         host="0.0.0.0",
         port=int(os.environ.get("PORT",5000)))
            
