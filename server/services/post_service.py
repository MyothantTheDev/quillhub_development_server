from flask_login import login_required
from server.utils.token_generator import jwt_required, adminauthorized_required

def trending_articles():...

@adminauthorized_required
@jwt_required
@login_required
def new_articles():...

def detail_article():...

@adminauthorized_required
@jwt_required
@login_required
def delete_article():...

@jwt_required
@login_required
def add_comment():...