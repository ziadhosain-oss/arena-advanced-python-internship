from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app import db
from app.models import User, Recipe, Category, Comment
from datetime import datetime

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipe')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ============= ADMIN DECORATOR =============
def admin_required(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# ============= MAIN ROUTES - USER SEQUENCE =============
@main_bp.route('/')
def index():
    """Homepage - Entry point for all users"""
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).paginate(page=page, per_page=6)
    categories = Category.query.all()
    return render_template('index.html', recipes=recipes, categories=categories)

@main_bp.route('/search')
def search():
    """Search recipes by title or ingredients"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if query:
        recipes = Recipe.query.filter(
            (Recipe.title.ilike(f'%{query}%')) | 
            (Recipe.description.ilike(f'%{query}%'))
        ).paginate(page=page, per_page=6)
    else:
        recipes = None
    
    return render_template('search.html', recipes=recipes, query=query)

@main_bp.route('/category/<int:category_id>')
def category(category_id):
    """View recipes by category - Discovery path"""
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.filter_by(category_id=category_id).paginate(page=page, per_page=6)
    return render_template('category.html', category=category, recipes=recipes)

@main_bp.route('/profile/<username>')
def profile(username):
    """View user profile and their recipes"""
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.filter_by(user_id=user.id).paginate(page=page, per_page=6)
    return render_template('profile.html', user=user, recipes=recipes)

# ============= AUTHENTICATION ROUTES =============
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('auth.register'))
        
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=bool(remember))
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

# ============= RECIPE ROUTES - CONSUMPTION SEQUENCE =============
@recipe_bp.route('/<int:recipe_id>')
def view(recipe_id):
    """View a single recipe - Consumption point"""
    recipe = Recipe.query.get_or_404(recipe_id)
    # Only show approved comments
    comments = Comment.query.filter_by(recipe_id=recipe_id, is_approved=True).order_by(Comment.created_at.desc()).all()
    avg_rating = db.session.query(db.func.avg(Comment.rating)).filter_by(recipe_id=recipe_id, is_approved=True).scalar()
    
    return render_template('recipe/view.html', recipe=recipe, comments=comments, avg_rating=avg_rating or 0)

@recipe_bp.route('/<int:recipe_id>/comment', methods=['POST'])
@login_required
def add_comment(recipe_id):
    """Add a comment to a recipe - Engagement point"""
    recipe = Recipe.query.get_or_404(recipe_id)
    
    content = request.form.get('content')
    rating = request.form.get('rating', 5, type=int)
    
    if not content:
        flash('Comment cannot be empty', 'error')
    else:
        comment = Comment(
            content=content,
            rating=min(5, max(1, rating)),
            user_id=current_user.id,
            recipe_id=recipe_id,
            is_approved=False  # Comments pending approval
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment submitted! It will appear after admin approval.', 'success')
    
    return redirect(url_for('recipe.view', recipe_id=recipe_id))

# ============= ADMIN ROUTES - BACKEND MANAGEMENT =============
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    recipes_count = Recipe.query.count()
    categories_count = Category.query.count()
    pending_comments = Comment.query.filter_by(is_approved=False).count()
    users_count = User.query.count()
    
    return render_template('admin/dashboard.html', 
                         recipes_count=recipes_count,
                         categories_count=categories_count,
                         pending_comments=pending_comments,
                         users_count=users_count)

# ============= ADMIN: CATEGORY MANAGEMENT =============
@admin_bp.route('/categories')
@login_required
@admin_required
def categories_list():
    """List all categories"""
    page = request.args.get('page', 1, type=int)
    categories = Category.query.paginate(page=page, per_page=10)
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/category/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_category():
    """Create new category"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Category name is required', 'error')
            return redirect(url_for('admin.create_category'))
        
        if Category.query.filter_by(name=name).first():
            flash('Category already exists', 'error')
            return redirect(url_for('admin.create_category'))
        
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        
        flash(f'Category "{name}" created successfully!', 'success')
        return redirect(url_for('admin.categories_list'))
    
    return render_template('admin/create_category.html')

@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    """Edit category"""
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.description = request.form.get('description')
        db.session.commit()
        
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin.categories_list'))
    
    return render_template('admin/edit_category.html', category=category)

@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    """Delete category"""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin.categories_list'))

# ============= ADMIN: RECIPE MANAGEMENT =============
@admin_bp.route('/recipes')
@login_required
@admin_required
def recipes_list():
    """List all recipes"""
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.paginate(page=page, per_page=10)
    return render_template('admin/recipes.html', recipes=recipes)

@admin_bp.route('/recipe/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_recipe():
    """Create new recipe - Admin only"""
    categories = Category.query.all()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        prep_time = request.form.get('prep_time', 0, type=int)
        cook_time = request.form.get('cook_time', 0, type=int)
        servings = request.form.get('servings', 1, type=int)
        category_id = request.form.get('category_id', type=int)
        
        if not title or not description or not ingredients or not instructions:
            flash('All fields are required', 'error')
            return redirect(url_for('admin.create_recipe'))
        
        recipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            prep_time=prep_time,
            cook_time=cook_time,
            servings=servings,
            category_id=category_id,
            user_id=current_user.id  # Admin as author
        )
        
        db.session.add(recipe)
        db.session.commit()
        
        flash('Recipe created successfully!', 'success')
        return redirect(url_for('admin.recipes_list'))
    
    return render_template('admin/create_recipe.html', categories=categories)

@admin_bp.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_recipe(recipe_id):
    """Edit recipe - Admin only"""
    recipe = Recipe.query.get_or_404(recipe_id)
    categories = Category.query.all()
    
    if request.method == 'POST':
        recipe.title = request.form.get('title')
        recipe.description = request.form.get('description')
        recipe.ingredients = request.form.get('ingredients')
        recipe.instructions = request.form.get('instructions')
        recipe.prep_time = request.form.get('prep_time', 0, type=int)
        recipe.cook_time = request.form.get('cook_time', 0, type=int)
        recipe.servings = request.form.get('servings', 1, type=int)
        recipe.category_id = request.form.get('category_id', type=int)
        recipe.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('admin.recipes_list'))
    
    return render_template('admin/edit_recipe.html', recipe=recipe, categories=categories)

@admin_bp.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_recipe(recipe_id):
    """Delete recipe - Admin only"""
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('admin.recipes_list'))

# ============= ADMIN: COMMENT MODERATION =============
@admin_bp.route('/comments')
@login_required
@admin_required
def comments_list():
    """List all comments for moderation"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pending')  # pending or approved
    
    if status == 'approved':
        comments = Comment.query.filter_by(is_approved=True).paginate(page=page, per_page=10)
    else:
        comments = Comment.query.filter_by(is_approved=False).paginate(page=page, per_page=10)
    
    return render_template('admin/comments.html', comments=comments, status=status)

@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_comment(comment_id):
    """Approve a comment - Moderation finalization"""
    comment = Comment.query.get_or_404(comment_id)
    comment.is_approved = True
    db.session.commit()
    
    flash('Comment approved!', 'success')
    return redirect(request.referrer or url_for('admin.comments_list'))

@admin_bp.route('/comment/<int:comment_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_comment(comment_id):
    """Reject/delete a comment"""
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    
    flash('Comment rejected!', 'success')
    return redirect(request.referrer or url_for('admin.comments_list'))

@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_comment(comment_id):
    """Delete an approved comment"""
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    
    flash('Comment deleted!', 'success')
    return redirect(request.referrer or url_for('admin.comments_list'))
