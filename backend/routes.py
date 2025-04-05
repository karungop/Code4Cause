from flask import Blueprint, request, jsonify
from models import db, Article
from datetime import datetime
from bs4 import BeautifulSoup
from utils import get_article_info  # if you moved it out


# Create a Blueprint for articles

def scrapper(url):
    results = get_article_info(url)  # Get article information (returns a dictionary)
    print(results)  # Debug print the results to ensure we get the expected output
    
    # Ensure all required fields are available before proceeding.
    title = results.get('Title')
    source = results.get('Source')
    description = results.get('Description')
    link = results.get('Link')
    
    # If any required fields are missing, return None.
    if not title or not source or not description:
        return None
    
    # Create an Article instance using the data from the dictionary.
    article = Article(
        title=title,
        author=source,  # Assuming source is used as author.
        content=description,  # Assuming description is the article content.
        topics=None,  # Set topics to None or extract if needed.
        link=link
    )
    
    # Add the article to the database session and commit.
    db.session.add(article)
    db.session.commit()
    
    return article  



articles_bp = Blueprint('articles', __name__)

@articles_bp.route('/articles/upload-url', methods=['POST'])
def upload_article_from_url():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    results = scrapper(url)

    print("Received URL:", url)
    print()
    #print(results)
    
    # you could add scraping logic here or just echo it back for now
    return jsonify({'message': 'URL received successfully', 'url': url}), 200


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