from flask import Blueprint, request, jsonify
from models import db, Article
from datetime import datetime
from werkzeug.utils import secure_filename 
from flask import Blueprint, request, jsonify
from openai import OpenAI
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
from datetime import datetime
import os
import openai
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('..') / '.env'  # Looks one level up
load_dotenv(dotenv_path=env_path)
# Create a Blueprint for articles

articles_bp = Blueprint('articles', __name__)

@articles_bp.route('/articles/upload-url', methods=['POST'])
def upload_article_from_url():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    print("Received URL:", url)
    # you could add scraping logic here or just echo it back for now
    return jsonify({'message': 'URL received successfully', 'url': url}), 200

UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@articles_bp.route('/articles/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file uploaded"}), 400
    
    pdf_file = request.files['pdf']
    
    if pdf_file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Save the file to the server's temp folder
    file_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_text = extract_text_from_pdf(file_path)
    if pdf_text:
        try:
            # Print the first 500 characters of the extracted text (for debugging)
            print("Extracted Text (First 500 chars): ", pdf_text[:500])

            # Limit text to stay within the token limit (approx. 4000 tokens for GPT-3.5)
            input_text = pdf_text[:2000]  # Adjust as needed

            # Send the extracted text to OpenAI for processing
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Or "gpt-4"
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Please process the text extracted from the PDF."},
                    {"role": "user", "content": input_text},
                ]
            )

            # Access the response correctly
            if 'choices' in response and len(response['choices']) > 0:
                result_text = response['choices'][0]['message']['content'].strip()
                print("Processed Text from OpenAI: ", result_text)
            else:
                print("No valid response from OpenAI.")
            
        except Exception as e:
            print(f"Error processing with OpenAI: {str(e)}")
    else:
        print("Failed to extract text from PDF.")
        pdf_file.save(file_path)

    # Now you can use `file_path` for scraping/processing!
    # Example: scrape_pdf(file_path)

    return jsonify({
        "message": "File uploaded successfully",
        "server_path": file_path,  # This is the path you can use
        "filename": pdf_file.filename,
        "size_bytes": os.path.getsize(file_path)
    })
# def upload_article_from_pdf():
#     # Check if PDF file was received
#     if 'pdf' not in request.files:
#         return jsonify({'error': 'No PDF file received'}), 400
    
#     pdf_file = request.files['pdf']
    
#     # Validate file
#     if pdf_file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400
    
#     if not pdf_file.filename.lower().endswith('.pdf'):
#         return jsonify({'error': 'Only PDF files are accepted'}), 400
    
#     try:
#         # Basic file information
#         file_size = len(pdf_file.read())
#         pdf_file.seek(0)  # Reset file pointer
        
#         # Simple confirmation response
#         return jsonify({
#             'status': 'success',
#             'message': 'PDF received successfully',
#             'details': {
#                 'filename': secure_filename(pdf_file.filename),
#                 'size_bytes': file_size,
#                 'received_at': datetime.utcnow().isoformat()
#             }
#         }), 200
        
#     except Exception as e:
#         return jsonify({
#             'error': f'Error processing PDF: {str(e)}'
#         }), 500



@articles_bp.route('/assessments/configure', methods=['POST'])
def configure_assessment():
    data = request.get_json()
    print("configure_assessment route hit!")  # ADD THIS

    config = {
        'total_questions': data.get('total_questions'),
        'mcq': data.get('mcq'),
        'short_answer': data.get('short_answer'),
        'long_answer': data.get('long_answer'),
        'require_verbal_summary': data.get('require_verbal_summary', False)
    }

    print("Received assessment config:", config)

    # You can add logic here to save it, validate it, or generate questions

    return jsonify({
        'message': 'Assessment configuration received',
        'config': config
    }), 200



@articles_bp.route('/articles', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    return jsonify([article.to_dict() for article in articles])

@articles_bp.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = Article.query.get_or_404(article_id)
    return jsonify(article.to_dict())

@articles_bp.route('/articles', methods=['POST'])
def create_article():
    data = request.get_json()
    
    if not all(key in data for key in ['title', 'author', 'content']):
        return jsonify({'error': 'Missing required fields'}), 400
    '''
    article = Article(
        title=data['title'],
        author=data['author'],
        content=data['content'],
        topics=data.get('topics', '')
    )
    
    db.session.add(article)
    db.session.commit()
    '''
    
    return jsonify(data), 201

@articles_bp.route('/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    article = Article.query.get_or_404(article_id)
    data = request.get_json()
    
    if 'title' in data:
        article.title = data['title']
    if 'author' in data:
        article.author = data['author']
    if 'content' in data:
        article.content = data['content']
    if 'topics' in data:
        article.topics = data['topics']
    
    db.session.commit()
    return jsonify(article.to_dict())

@articles_bp.route('/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({'message': 'Article deleted'}), 200

@articles_bp.route('/articles/search', methods=['GET'])
def search_articles():
    topic = request.args.get('topic')
    if not topic:
        return jsonify({'error': 'No topic provided'}), 400
    
    articles = Article.query.filter(Article.topics.contains(topic)).all()
    return jsonify([article.to_dict() for article in articles])

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_path):
    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)
        
        # Initialize an empty string to store the extracted text
        full_text = ""
        
        # Extract text from each page
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            full_text += page.get_text()
        
        return full_text
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return None
