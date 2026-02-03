import mysql.connector
import sys

def setup_database():
    print("🚀 Setting up Business Dashboard Database...")
    print("=" * 50)
    
    try:
        # Connect to MySQL (WAMP default: no password)
        print("Connecting to MySQL...")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Empty password for WAMP
            charset="utf8mb4"
        )
        
        cursor = conn.cursor()
        
        # Create database
        print("Creating database 'business_dashboard'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS business_dashboard")
        cursor.execute("USE business_dashboard")
        
        # Read setup.sql file
        print("Reading setup.sql...")
        with open("database/setup.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()
        
        # Split and execute SQL commands
        print("Executing SQL commands...")
        commands = sql_script.split(';')
        
        for i, command in enumerate(commands):
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    print(f"  ✓ Command {i+1} executed")
                except mysql.connector.Error as err:
                    print(f"  ⚠️ Command {i+1} warning: {err}")
        
        conn.commit()
        print("\n" + "=" * 50)
        print("✅ Database setup COMPLETE!")
        print("\nDefault login credentials:")
        print("  👑 Admin: admin / admin123")
        print("  👥 Staff: staff1 / password123")
        print("\nAccess your app at: http://localhost:5000")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"\n❌ ERROR: {err}")
        print("\nTroubleshooting:")
        print("1. Is WAMP running? (Check for GREEN icon)")
        print("2. Try: http://localhost/phpmyadmin")
        print("3. WAMP MySQL default has NO password")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()