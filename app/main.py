from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Document
from . import db

main = Blueprint('main', __name__)

CATEGORIES = [
    'AGI', 'ACTF', '수영', '스카이다이빙', '암벽등반', '카페 취업', '기술 연마'
]

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/category/<cat_name>')
@login_required
def category(cat_name):
    if cat_name not in CATEGORIES:
        return "Category not found", 404
    docs = Document.query.filter_by(category=cat_name).order_by(Document.created_at.desc()).all()
    return render_template('content/category.html', category=cat_name, docs=docs)

@main.route('/create', methods=['GET', 'POST'])
@login_required
def create_doc():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')

        if not title or not content or category not in CATEGORIES:
            flash('모든 필드를 올바르게 입력해주세요.')
            return redirect(url_for('main.create_doc'))

        new_doc = Document(title=title, content=content, category=category, author_id=current_user.id)
        db.session.add(new_doc)
        db.session.commit()

        return redirect(url_for('main.category', cat_name=category))

    return render_template('content/create.html', categories=CATEGORIES)

@main.route('/profile')
@login_required
def profile():
    user_docs = Document.query.filter_by(author_id=current_user.id).all()
    return render_template('profile.html', name=current_user.name, docs=user_docs)
