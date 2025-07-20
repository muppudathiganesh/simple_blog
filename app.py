from flask import Flask, render_template, request, redirect, url_for
import json
import uuid

app = Flask(__name__)

POST_FILE = 'posts.json'

def load_posts():
    try:
        with open(POST_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_post(post):
    posts = load_posts()
    posts.append(post)
    with open(POST_FILE, 'w') as f:
        json.dump(posts, f, indent=2)

@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts[::-1])

@app.route('/post/<post_id>')
def post(post_id):
    posts = load_posts()
    for p in posts:
        if p['id'] == post_id:
            return render_template('post.html', post=p)
    return "Post not found", 404

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = {
            'id': str(uuid.uuid4()),
            'title': title,
            'content': content
        }
        save_post(new_post)
        return redirect(url_for('index'))
    return render_template('admin.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    posts = load_posts()
    results = [p for p in posts if query in p['title'].lower() or query in p['content'].lower()]
    return render_template('search.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)