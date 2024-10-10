#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles',methods=['GET'])
def index_articles():
    articles=Article.query.all()
    article_list=[article.to_dict()for article in articles]
    return jsonify (article_list),200


@app.route('/articles/<int:id>',methods=['GET'])
def show_article(id):
   # Set an initial value of 0 for 'page_views' if it doesn't exist
    session['page_views'] = session.get('page_views', 0) + 1
    
    # Check if the user has exceeded the page view limit
    if session['page_views'] <= 3:
        # Return the article data if within limit
        article =Article.query.get(id)
        if article:
            return jsonify(article.to_dict()), 200
        else:
            return jsonify({"message": "Article not found"}), 404
    else:
        # If the limit is exceeded, return an error message
        return jsonify({"message": "Maximum pageview limit reached"}), 401

if __name__ == '__main__':
    app.run(port=5555)
