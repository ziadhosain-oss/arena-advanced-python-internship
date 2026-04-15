# Recipe Sharing Website 🍳

A Flask-based recipe sharing platform where users can create, browse, and discuss recipes with ratings and comments.

## Features

### User Authentication
- User registration and login system
- Password hashing for security
- User profiles with activity history
- OAuth-ready architecture

### Recipe Management
- **Create Recipes**: Users can add new recipes with ingredients and instructions
- **Edit & Delete**: Modify or remove your own recipes
- **Rich Recipe Details**: 
  - Prep and cook time tracking
  - Serving sizes
  - Step-by-step instructions
  - Ingredient lists
  - Category organization

### Social Features
- **Comments & Ratings**: Leave comments and 1-5 star ratings on recipes
- **User Profiles**: View other users' recipe collections
- **Follow Categories**: Browse recipes by category (Breakfast, Lunch, Dinner, etc.)

### Discovery
- **Search Functionality**: Find recipes by title or description
- **Category Browsing**: Explore recipes by meal type
- **Featured Recipes**: Homepage showcases latest recipes
- **Pagination**: Browse large recipe collections easily

### Built With
- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite
- **Authentication**: Flask-Login
- **Frontend**: HTML5, CSS3, Jinja2 templates
- **Styling**: Responsive CSS with modern design

## Project Structure

```
recipe_sharing_website/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models (User, Recipe, Comment, Category)
│   ├── routes.py                # Application routes and views
│   ├── static/
│   │   └── css/
│   │       └── style.css        # Application styling
│   └── templates/
│       ├── base.html            # Base template with navigation
│       ├── index.html           # Homepage
│       ├── search.html          # Search results
│       ├── category.html        # Category view
│       ├── profile.html         # User profile
│       ├── auth/
│       │   ├── login.html       # Login page
│       │   └── register.html    # Registration page
│       └── recipe/
│           ├── create.html      # Create recipe form
│           ├── edit.html        # Edit recipe form
│           └── view.html        # Recipe details page
├── config.py                    # Configuration settings
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
cd recipe_sharing_website
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python run.py
```

The application will start on `http://127.0.0.1:5000`

## Usage

### First Time Setup
1. Navigate to http://127.0.0.1:5000 in your browser
2. Click "Register" to create a new account
3. Fill in your username, email, and password
4. Log in with your credentials

### Creating Your First Recipe
1. Click "+ New Recipe" in the navigation bar
2. Fill in the recipe details:
   - Title and description
   - Prep time and cook time
   - Number of servings
   - Select a category
   - List ingredients (one per line)
   - Add step-by-step instructions
3. Click "Create Recipe"

### Interacting with Recipes
- **View**: Click any recipe card to see full details
- **Search**: Use the search bar to find recipes by name or description
- **Comment**: Add comments and ratings to recipes
- **Browse**: Choose a category to see recipes in that category
- **Profile**: Visit user profiles to see their recipes

### Recipe Management
- **Edit**: Go to your recipe and click "Edit Recipe" to modify it
- **Delete**: Click "Delete Recipe" to remove it (cannot be undone)
- **Delete Comments**: Recipe authors and comment authors can delete comments

## Database Models

### User
- Username (unique)
- Email (unique)
- Password hash
- Bio
- Created timestamp

### Recipe
- Title
- Description
- Ingredients (stored as newline-separated text)
- Instructions (stored as newline-separated text)
- Prep time (minutes)
- Cook time (minutes)
- Servings
- Category
- Author (references User)
- Created/Updated timestamps

### Comment
- Content
- Rating (1-5 stars)
- Author (references User)
- Recipe (references Recipe)
- Created/Updated timestamps

### Category
- Name (unique)
- Description

## Configuration

Edit `config.py` to customize:

```python
SECRET_KEY          # Change this in production!
SQLALCHEMY_DATABASE_URI  # Database connection string
SESSION_COOKIE_SECURE    # Set to True for HTTPS
SESSION_COOKIE_HTTPONLY  # Secure cookie settings
```

## Sample Categories

The application auto-initializes with the following categories:
- Breakfast
- Lunch
- Dinner
- Desserts
- Beverages
- Appetizers
- Salads
- Soups

## API Routes

### Main Routes
- `GET /` - Homepage with featured recipes
- `GET /search?q=<query>` - Search recipes
- `GET /category/<id>` - View recipes by category
- `GET /profile/<username>` - View user profile

### Authentication Routes
- `GET/POST /auth/register` - User registration
- `GET/POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Recipe Routes
- `GET/POST /recipe/create` - Create new recipe
- `GET /recipe/<id>` - View recipe details
- `GET/POST /recipe/<id>/edit` - Edit recipe
- `POST /recipe/<id>/delete` - Delete recipe
- `POST /recipe/<id>/comment` - Add comment
- `POST /recipe/comment/<id>/delete` - Delete comment

## Security Notes

⚠️ **Important for Production:**
1. Change `SECRET_KEY` in `config.py`
2. Set `DEBUG = False` in production
3. Use `SESSION_COOKIE_SECURE = True` with HTTPS
4. Set up a proper database (PostgreSQL recommended)
5. Use environment variables for sensitive data
6. Add rate limiting to prevent abuse
7. Implement CSRF protection (Flask-WTF already included)

## Future Enhancements

Potential features for future versions:
- Image upload for recipes
- Recipe ratings system
- Favorite/bookmark recipes
- Following system for users
- Recipe difficulty levels
- Nutritional information
- Print-friendly recipe format
- Social sharing (Facebook, Twitter)
- Email notifications
- Dietary restrictions/allergies
- Advanced search filters
- Admin dashboard
- Recipe collections/folders

## Troubleshooting

### Database Issues
If you encounter database errors:
```bash
# Delete the existing database
cd recipe_sharing_website
rm instance/recipe_sharing.db

# Restart the application
python run.py
```

### Port Already in Use
If port 5000 is already in use, edit `run.py`:
```python
app.run(debug=True, port=5001)  # Change to different port
```

### Template Not Found
Ensure all template files are in the correct directories:
- `app/templates/` - Main templates
- `app/templates/auth/` - Authentication templates
- `app/templates/recipe/` - Recipe templates

## Development

### Running in Development Mode
The application runs with `debug=True` by default, which enables:
- Auto-reloading on code changes
- Interactive debugger
- Detailed error messages

### Creating Database Entries Manually
```python
python
>>> from run import app, db
>>> from app.models import User, Recipe, Category
>>> with app.app_context():
...     user = User(username='test', email='test@example.com')
...     user.set_password('password123')
...     db.session.add(user)
...     db.session.commit()
```

## License

This project is open source and available under the MIT License.

## Contact & Support

For issues, questions, or suggestions, please feel free to open an issue or contact the development team.

---

Enjoy sharing your favorite recipes! 🍽️👨‍🍳
