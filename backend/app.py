from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Article
from routes import articles_bp  # Add this import at the top

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(articles_bp, url_prefix='/api')  # Optional url_prefix

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Articles API",
        "endpoints": {
            "get_articles": "GET /api/articles",
            "create_article": "POST /api/articles",
            "get_article": "GET /api/articles/<id>"
        }
    })

@app.route('/api/articles', methods=['GET', 'POST'])
def handle_articles():
    if request.method == 'GET':
        articles = Article.query.all()
        return jsonify([article.to_dict() for article in articles])
    
    if request.method == 'POST':
        data = request.get_json()
        article = Article(
            title=data['title'],
            author=data['author'],
            content=data['content'],
            topics=data.get('topics', '')
        )
        db.session.add(article)
        db.session.commit()
        return jsonify(article.to_dict()), 201

@app.route('/api/articles/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_article(id):
    article = Article.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify(article.to_dict())
    
    if request.method == 'PUT':
        data = request.get_json()
        article.title = data.get('title', article.title)
        article.author = data.get('author', article.author)
        article.content = data.get('content', article.content)
        article.topics = data.get('topics', article.topics)
        db.session.commit()
        return jsonify(article.to_dict())
    
    if request.method == 'DELETE':
        db.session.delete(article)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)