#!/usr/bin/env python
"""
Entry point for the Recipe Sharing Website Flask application
"""

from app import create_app, db
from app.models import User, Recipe, Category, Comment

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Create shell context for Flask CLI"""
    return {'db': db, 'User': User, 'Recipe': Recipe, 'Category': Category, 'Comment': Comment}

if __name__ == '__main__':
    # Initialize database with sample data on first run
    with app.app_context():
        # Check if categories exist
        if Category.query.count() == 0:
            categories = [
                Category(name='Breakfast', description='Start your day right with our breakfast recipes'),
                Category(name='Lunch', description='Delicious lunch ideas for work or home'),
                Category(name='Dinner', description='Hearty dinner recipes for the whole family'),
                Category(name='Desserts', description='Sweet treats and desserts'),
                Category(name='Beverages', description='Drinks and beverages'),
                Category(name='Appetizers', description='Starters and appetizers'),
                Category(name='Salads', description='Fresh and healthy salad recipes'),
                Category(name='Soups', description='Comforting soup recipes'),
            ]
            db.session.add_all(categories)
            db.session.commit()
            print("✓ Sample categories added to database")
        
        # Create default admin user if it doesn't exist
        if User.query.filter_by(username='admin').first() is None:
            admin = User(username='admin', email='admin@recipeapp.local', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created")
            print("  Username: admin")
            print("  Password: admin123")
            print("  → Change this password after first login!")
        
        # Create sample recipes if none exist
        if Recipe.query.count() == 0:
            admin = User.query.filter_by(username='admin').first()
            breakfast_cat = Category.query.filter_by(name='Breakfast').first()
            lunch_cat = Category.query.filter_by(name='Lunch').first()
            dinner_cat = Category.query.filter_by(name='Dinner').first()
            dessert_cat = Category.query.filter_by(name='Desserts').first()
            
            sample_recipes = [
                Recipe(
                    title='Fluffy Pancakes',
                    description='Delicious fluffy pancakes perfect for a weekend breakfast with fresh berries and maple syrup.',
                    ingredients='2 cups flour\n2 tablespoons sugar\n2 teaspoons baking powder\n1 teaspoon salt\n2 cups milk\n2 eggs\n2 tablespoons melted butter',
                    instructions='Mix dry ingredients in a bowl\nAdd wet ingredients and stir until combined\nCook on griddle over medium heat\nFlip when bubbles appear\nServe warm with toppings',
                    prep_time=10,
                    cook_time=15,
                    servings=4,
                    category_id=breakfast_cat.id,
                    user_id=admin.id,
                    image_url='data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="200"%3E%3Crect fill="%23FFD700" width="300" height="200"/%3E%3Ctext x="50%25" y="50%25" font-size="80" text-anchor="middle" dominant-baseline="middle"%3E🥞%3C/text%3E%3C/svg%3E'
                ),
                Recipe(
                    title='Caesar Salad',
                    description='Classic Caesar salad with crisp romaine lettuce, parmesan cheese, and homemade croutons.',
                    ingredients='8 cups romaine lettuce\n1/2 cup parmesan cheese\n1 cup croutons\n4 anchovy fillets\n1/2 cup mayonnaise\n2 tablespoons lemon juice',
                    instructions='Wash and chop romaine lettuce\nMake dressing with mayonnaise and anchovy\nToss lettuce with dressing\nAdd croutons and parmesan\nServe immediately',
                    prep_time=15,
                    cook_time=0,
                    servings=2,
                    category_id=lunch_cat.id,
                    user_id=admin.id,
                    image_url='data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="200"%3E%3Crect fill="%2390EE90" width="300" height="200"/%3E%3Ctext x="50%25" y="50%25" font-size="80" text-anchor="middle" dominant-baseline="middle"%3E🥗%3C/text%3E%3C/svg%3E'
                ),
                Recipe(
                    title='Spaghetti Carbonara',
                    description='Authentic Italian pasta with eggs, cheese, guanciale, and black pepper - simple but delicious!',
                    ingredients='1 lb spaghetti\n5 oz guanciale\n4 eggs\n2 cups pecorino romano cheese\nBlack pepper to taste\nSalt for pasta water',
                    instructions='Cook spaghetti in salted boiling water\nFry guanciale until crispy\nWhisk eggs with cheese and pepper\nDrain pasta and toss with guanciale\nAdd egg mixture off heat and toss quickly\nServe immediately',
                    prep_time=5,
                    cook_time=20,
                    servings=4,
                    category_id=dinner_cat.id,
                    user_id=admin.id,
                    image_url='data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="200"%3E%3Crect fill="%23DAA520" width="300" height="200"/%3E%3Ctext x="50%25" y="50%25" font-size="80" text-anchor="middle" dominant-baseline="middle"%3E🍝%3C/text%3E%3C/svg%3E'
                ),
                Recipe(
                    title='Chocolate Brownies',
                    description='Rich, fudgy chocolate brownies that are perfect for chocolate lovers. Serve warm with ice cream!',
                    ingredients='1 cup butter\n8 oz dark chocolate\n2 cups sugar\n4 eggs\n1 cup flour\n1/2 teaspoon salt\n1 teaspoon vanilla extract',
                    instructions='Preheat oven to 350°F\nMelt butter and chocolate together\nMix sugar and eggs until combined\nAdd chocolate mixture\nFold in flour and salt\nPour into baking pan\nBake for 25-30 minutes',
                    prep_time=15,
                    cook_time=30,
                    servings=12,
                    category_id=dessert_cat.id,
                    user_id=admin.id,
                    image_url='data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="200"%3E%3Crect fill="%238B4513" width="300" height="200"/%3E%3Ctext x="50%25" y="50%25" font-size="80" text-anchor="middle" dominant-baseline="middle"%3E🍫%3C/text%3E%3C/svg%3E'
                ),
                Recipe(
                    title='Grilled Salmon',
                    description='Herb-crusted grilled salmon with lemon and garlic. A healthy and elegant dinner option.',
                    ingredients='4 salmon fillets\n4 tablespoons olive oil\n4 garlic cloves\n2 lemons\nFresh herbs (dill, parsley)\nSalt and pepper',
                    instructions='Prepare grill to medium-high heat\nMix oil with minced garlic and herbs\nSeason salmon with salt and pepper\nRub with herb mixture\nGrill for 5-7 minutes per side\nServe with lemon wedges',
                    prep_time=15,
                    cook_time=15,
                    servings=4,
                    category_id=dinner_cat.id,
                    user_id=admin.id,
                    image_url='data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="200"%3E%3Crect fill="%23CD5C5C" width="300" height="200"/%3E%3Ctext x="50%25" y="50%25" font-size="80" text-anchor="middle" dominant-baseline="middle"%3E🐟%3C/text%3E%3C/svg%3E'
                ),
            ]
            db.session.add_all(sample_recipes)
            db.session.commit()
            print(f"✓ Sample recipes created: {len(sample_recipes)} recipes added")
    
    print("\n🍳 Recipe Sharing Website is starting...")
    print("🔗 Visit http://127.0.0.1:5000 in your browser")
    print("\n📋 USER SEQUENCE:")
    print("   1. Home → Browse Recipes")
    print("   2. Categories → Filter by Type")
    print("   3. Search → Find Recipes")
    print("   4. Recipe → View & Comment")
    print()
    print("⚙️  ADMIN SEQUENCE (Access via /admin/dashboard):")
    print("   • Manage Categories")
    print("   • Create/Edit/Delete Recipes")
    print("   • Moderate Comments")
    print("\nTo stop the server, press CTRL+C\n")
    
    app.run(debug=True)
