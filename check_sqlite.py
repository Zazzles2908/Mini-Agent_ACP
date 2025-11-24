import sqlite3
import os

# Check SQLite database contents
db_path = './workspace/enhanced_memory.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check table structure
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='notes'")
    table_info = cursor.fetchone()
    print('Table exists:', table_info is not None)
    
    # Check note count
    cursor.execute('SELECT COUNT(*) FROM notes')
    count = cursor.fetchone()[0]
    print(f'Total notes: {count}')
    
    # Check if any enhanced notes
    cursor.execute('SELECT COUNT(*) FROM notes WHERE enhanced = 1')
    enhanced_count = cursor.fetchone()[0]
    print(f'Enhanced notes: {enhanced_count}')
    
    conn.close()
else:
    print('Database does not exist')
