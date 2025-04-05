from flask import Blueprint, request, jsonify
from models import db, Article
from datetime import datetime
from werkzeug.utils import secure_filename 
from flask import Blueprint, request, jsonify
import fitz 

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

@articles_bp.route('/articles/upload-pdf', methods=['POST'])
def upload_article_from_pdf():
    # Check if PDF file was received
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file received'}), 400
    
    pdf_file = request.files['pdf']
    
    # Validate file
    if pdf_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not pdf_file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are accepted'}), 400
    
    try:
        # Basic file information
        file_size = len(pdf_file.read())
        pdf_file.seek(0)  # Reset file pointer
        
        # Simple confirmation response
        return jsonify({
            'status': 'success',
            'message': 'PDF received successfully',
            'details': {
                'filename': secure_filename(pdf_file.filename),
                'size_bytes': file_size,
                'received_at': datetime.utcnow().isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error processing PDF: {str(e)}'
        }), 500



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