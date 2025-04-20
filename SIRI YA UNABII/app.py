from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Database setup
def init_db():
    if not os.path.exists('data'):
        os.makedirs('data')
    
    conn = sqlite3.connect('data/books.db')
    c = conn.cursor()
    
    # Create tables if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 filename TEXT NOT NULL,
                 cover_image TEXT NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS views
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 book_id INTEGER NOT NULL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY (book_id) REFERENCES books (id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS downloads
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 book_id INTEGER NOT NULL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY (book_id) REFERENCES books (id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 email TEXT NOT NULL,
                 subject TEXT NOT NULL,
                 message TEXT NOT NULL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Insert sample books if they don't exist
    books = [
        ("Alama Ya Mnyama", "alama-ya-mnyama.pdf", "alama-ya-mnyama.jpg"),
        ("Wafu Wako Wapi", "wafu-wako-wapi.pdf", "wafu-wako-wapi.jpg"),
        ("Nyimbo Za Krisito SDA", "nyimbo-za-krisito-sda.pdf", "nyimbo-za-krisito-sda.jpg"),
        ("Roho Mtakatifu", "roho-mtakatifu.pdf", "roho-mtakatifu.jpg"),
        ("Mpango Wa Usomaji Biblia Kwa Mwaka", "mpango-wa-usomaji-biblia.pdf", "mpango-wa-usomaji-biblia.jpg"),
        ("Siku 10 Za Maombi 2023 Kurejea Madhabahuni", "siku-10-za-maombi.pdf", "siku-10-za-maombi.jpg"),
        ("Juma La Maombi – November 2022 Wanafunzi Wanaokua", "juma-la-maombi.pdf", "juma-la-maombi.jpg")
    ]
    
    for book in books:
        c.execute("SELECT id FROM books WHERE title=?", (book[0],))
        if not c.fetchone():
            c.execute("INSERT INTO books (title, filename, cover_image) VALUES (?, ?, ?)", book)
    
    conn.commit()
    conn.close()

init_db()

# API Routes 1
@app.route('/api/books', methods=['GET'])
def get_books():
    conn = sqlite3.connect('data/books.db')
    c = conn.cursor()
    
    c.execute('''SELECT b.id, b.title, b.filename, b.cover_image, 
                 COUNT(v.id) as views, COUNT(d.id) as downloads
                 FROM books b
                 LEFT JOIN views v ON b.id = v.book_id
                 LEFT JOIN downloads d ON b.id = d.book_id
                 GROUP BY b.id''')
    
    books = []
    for row in c.fetchall():
        books.append({
            'id': row[0],
            'title': row[1],
            'filename': row[2],
            'cover_image': row[3],
            'views': row[4],
            'downloads': row[5]
        })
    
    conn.close()
    return jsonify(books)

@app.route('/api/track-view', methods=['POST'])
def track_view():
    data = request.get_json()
    book_id = data.get('bookId')
    
    if not book_id:
        return jsonify({'error': 'Book ID is required'}), 400
    
    conn = sqlite3.connect('data/books.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO views (book_id) VALUES (?)", (book_id,))
    conn.commit()
    
    c.execute("SELECT COUNT(id) FROM views WHERE book_id=?", (book_id,))
    views_count = c.fetchone()[0]
    
    conn.close()
    return jsonify({'success': True, 'views': views_count})

@app.route('/api/track-download', methods=['POST'])
def track_download():
    data = request.get_json()
    book_id = data.get('bookId')
    
    if not book_id:
        return jsonify({'error': 'Book ID is required'}), 400
    
    conn = sqlite3.connect('data/books.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO downloads (book_id) VALUES (?)", (book_id,))
    conn.commit()
    
    c.execute("SELECT COUNT(id) FROM downloads WHERE book_id=?", (book_id,))
    downloads_count = c.fetchone()[0]
    
    conn.close()
    return jsonify({'success': True, 'downloads': downloads_count})

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')
    
    if not all([name, email, subject, message]):
        return jsonify({'error': 'All fields are required'}), 400
    
    conn = sqlite3.connect('data/books.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO contacts (name, email, subject, message) VALUES (?, ?, ?, ?)",
              (name, email, subject, message))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# Serve book files
@app.route('/books/<filename>', methods=['GET'])
def serve_book(filename):
    return send_from_directory('books', filename)

# Serve images
@app.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    app.run(debug=True)
    
   # class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('+255767352878'))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime)

def calculate_earnings(views):
    # Implement your payment calculation logic
    return views * 0.01  # Example: $0.01 per view 

app = Flask(__name__)

# Example email regex for validation
EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email', '').strip()

    # Validate email
    if not re.match(EMAIL_REGEX, email):
        return jsonify({'success': False, 'message': 'Invalid email address.'}), 400

    # Save the email to your database or mailing list here
    # For example, append to a file:
    try:
        with open('subscribers.txt', 'a') as f:
            f.write(email + '\n')
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to save email.'}), 500

if __name__=='__main__':
     app.run(debug=true)