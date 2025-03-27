from flask import request, jsonify
from server.models.article import Article, ArticleBlock
from flask_login import current_user, login_required
from server.middleware.token_generator import jwt_required, adminauthorized_required
import json

def trending_articles():...

def detail_article():...

@adminauthorized_required
@jwt_required
@login_required
def delete_article():...

@jwt_required
@login_required
def add_comment():...