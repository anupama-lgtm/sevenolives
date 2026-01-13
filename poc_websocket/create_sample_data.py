#!/usr/bin/env python
"""
Script to create sample data for testing
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poc_project.settings')
django.setup()

from user_app.models import User

def create_sample_data():
    """Create sample users"""
    
    # Clear existing data
    User.objects.all().delete()
    
    # Create sample users
    users = [
        {'first_name': 'John', 'last_name': 'Doe'},
        {'first_name': 'Jane', 'last_name': 'Smith'},
        {'first_name': 'Alice', 'last_name': 'Johnson'},
        {'first_name': 'Bob', 'last_name': 'Williams'},
    ]
    
    for user_data in users:
        user = User.objects.create(**user_data)
        print(f"✓ Created user: {user.first_name} {user.last_name} (ID: {user.id})")
    
    print(f"\n✓ Successfully created {len(users)} sample users!")

if __name__ == '__main__':
    print("========================================")
    print("Creating Sample Data...")
    print("========================================\n")
    create_sample_data()

