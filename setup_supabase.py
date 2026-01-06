"""
Helper script to set up Supabase database connection and run migrations.
This script helps configure your Django app to use Supabase.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Weighing.settings')
django.setup()

from django.core.management import execute_from_command_line

def main():
    """
    Set up Supabase database connection.
    Make sure DATABASE_URL environment variable is set before running.
    """
    print("=" * 60)
    print("Supabase Database Setup")
    print("=" * 60)
    print()
    
    # Check if DATABASE_URL is set
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("⚠️  DATABASE_URL environment variable is not set!")
        print()
        print("Your Supabase project URL: https://pnzqqidifdqanknakpov.supabase.co")
        print()
        print("To get your connection string:")
        print("1. Go to https://supabase.com/dashboard/project/pnzqqidifdqanknakpov")
        print("2. Navigate to Settings → Database")
        print("3. Copy the connection string (URI format)")
        print("4. Set it as an environment variable:")
        print("   Windows PowerShell:")
        print('   $env:DATABASE_URL="postgresql://postgres:[PASSWORD]@db.pnzqqidifdqanknakpov.supabase.co:5432/postgres"')
        print("   Linux/Mac:")
        print('   export DATABASE_URL="postgresql://postgres:[PASSWORD]@db.pnzqqidifdqanknakpov.supabase.co:5432/postgres"')
        print()
        return
    
    print(f"✅ DATABASE_URL is set")
    print(f"   Connection: {database_url.split('@')[1] if '@' in database_url else 'Hidden'}")
    print()
    
    # Run migrations
    print("Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully!")
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return
    
    print()
    print("=" * 60)
    print("Setup complete! Your Django app is now connected to Supabase.")
    print("=" * 60)

if __name__ == '__main__':
    main()

