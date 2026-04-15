# Flask Web Scraper App with Role-Based Access Control

A Flask web application that scrapes product data and provides role-based access control for users and administrators.

## Features

### User Roles
- **Admin**: Full access to all functionalities including user management, product management, and scraping
- **User**: Can login, view products, and favorite/unfavorite products

### Role-Based Access Control
1. ✅ Create roles (admin and user)
2. ✅ Allow non-admin users to login
3. ✅ Non-admin users cannot access /admin route
4. ✅ Non-admin users cannot access admin functionalities
5. ✅ Users can favorite and unfavorite products
6. ✅ Admin can continue existing functionalities (manage products, users, scraping)

## Installation

1. Install Python dependencies:
```bash
pip install flask pymongo requests beautifulsoup4
```

2. Install and start MongoDB on localhost:27017

3. Run the application:
```bash
python app.py
```

4. Initialize the database by visiting: `http://localhost:5000/init_db`
   - This creates default users:
     - Admin: username `admin`, password `admin`

## Usage

### For Users
- Login with user credentials
- View all scraped products
- Favorite/unfavorite products
- Cannot access admin panel

### For Admins
- Login with admin credentials
- Access admin panel at `/admin`
- View all products and users
- Delete products
- Run web scraper
- Manage users (create/delete users)
- All user functionalities

## Routes

### Public Routes
- `/` - Home page with products
- `/login` - Login (POST)
- `/logout` - Logout
- `/init_db` - Initialize database with default users

### User Routes
- `/toggle_favorite/<product_id>` - Toggle favorite status for a product

### Admin Routes (require @admin_required decorator)
- `/admin` - Admin panel
- `/admin/delete_product/<product_id>` - Delete a product
- `/scrape` - Run web scraper
- `/admin/users` - User management page
- `/admin/create_user` - Create new user (POST)
- `/admin/delete_user/<user_id>` - Delete a user

## Security Features
- Session-based authentication
- Role-based access control with `@admin_required` decorator
- Password-based login
- Admin-only routes protected
- CSRF protection via Flask-WTF (not implemented yet)

## Database Schema

### Users Collection
```json
{
  "username": "string",
  "password": "string", 
  "role": "admin" | "user",
  "favorites": ["product_id1", "product_id2", ...]
}
```

### Products Collection
```json
{
  "_id": ObjectId,
  "name": "string",
  "price": "string",
  "product_url": "string"
}
```