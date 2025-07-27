from flask import Flask, render_template_string, request, redirect, url_for
import time
import random
import os
import json

app = Flask(__name__)

# File-based storage for better persistence
DATA_FILE = 'data.json'

# Initialize storage
def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                return data.get('businesses', []), data.get('submissions', [])
    except Exception as e:
        print(f"Error loading data: {e}")
    return [], []

def save_data(businesses, submissions):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump({'businesses': businesses, 'submissions': submissions}, f)
    except Exception as e:
        print(f"Error saving data: {e}")

# Load initial data
businesses, submissions = load_data()

# Define directories
directories = [
    {"name": "Google Business Profile", "category": "Major", "success_rate": 0.95},
    {"name": "Bing Places", "category": "Major", "success_rate": 0.90},
    {"name": "Yelp", "category": "Major", "success_rate": 0.85},
    {"name": "Facebook", "category": "Social", "success_rate": 0.92},
    {"name": "Apple Maps", "category": "Major", "success_rate": 0.88}
]

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Directory Blast</title>
        <style>
            body { font-family: Arial; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: white; }
            .container { max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; }
            h1 { text-align: center; margin-bottom: 30px; }
            .btn { background: #2ecc71; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; }
            .center { text-align: center; margin-top: 30px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Directory Blast</h1>
            <p>Submit your business to multiple directories with one click. Boost your local SEO instantly.</p>
            <div class="center">
                <a href="/add-business" class="btn">Add Your Business</a>
                <a href="/dashboard" class="btn" style="background: #3498db; margin-left: 10px;">View Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/dashboard')
def dashboard():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - Directory Blast</title>
        <style>
            body { font-family: Arial; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #333; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; }
            h1 { text-align: center; color: #764ba2; margin-bottom: 30px; }
            .stats { display: flex; justify-content: space-around; margin-bottom: 30px; }
            .stat-box { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; width: 30%; }
            .stat-number { font-size: 2rem; font-weight: bold; color: #764ba2; }
            .business-list { margin-top: 30px; }
            .business-card { background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
            .business-name { margin-top: 0; color: #764ba2; }
            .btn { background: #764ba2; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; display: inline-block; }
            .no-business { text-align: center; margin: 50px 0; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Directory Blast Dashboard</h1>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{{ businesses|length }}</div>
                    <div>Businesses</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{{ submissions|length }}</div>
                    <div>Submissions</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{{ success_rate }}%</div>
                    <div>Success Rate</div>
                </div>
            </div>
            
            <div class="business-list">
                <h2>Your Businesses</h2>
                
                {% if businesses %}
                    {% for business in businesses %}
                    <div class="business-card">
                        <h3 class="business-name">{{ business.name }}</h3>
                        <p>{{ business.address }} • {{ business.phone }}</p>
                        <a href="/submit-business/{{ business.id }}" class="btn">Submit to Directories</a>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="no-business">
                        <p>No businesses added yet.</p>
                        <a href="/add-business" class="btn">Add Your First Business</a>
                    </div>
                {% endif %}
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <a href="/add-business" class="btn" style="background: #2ecc71;">Add New Business</a>
                <a href="/" class="btn" style="background: #3498db; margin-left: 10px;">Home</a>
            </div>
        </div>
    </body>
    </html>
    ''', 
    businesses=businesses, 
    submissions=submissions, 
    success_rate=int(sum(1 for s in submissions if s.get('status') == 'success') / max(len(submissions), 1) * 100) if submissions else 0)

@app.route('/add-business', methods=['GET', 'POST'])
def add_business():
    global businesses
    
    if request.method == 'POST':
        try:
            # Generate ID safely
            new_id = 1
            if businesses:
                new_id = max(b.get('id', 0) for b in businesses) + 1
                
            business = {
                'id': new_id,
                'name': request.form['name'],
                'category': request.form['category'],
                'address': request.form['address'],
                'phone': request.form['phone'],
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            businesses.append(business)
            save_data(businesses, submissions)
            return redirect(url_for('submit_business', business_id=business['id']))
        except Exception as e:
            return f"Error adding business: {str(e)}", 500
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Business</title>
        <style>
            body { font-family: Arial; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #333; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            h1 { text-align: center; margin-bottom: 30px; color: #764ba2; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
            .btn { background: #764ba2; color: white; padding: 12px; border: none; border-radius: 5px; width: 100%; font-size: 16px; cursor: pointer; }
            .btn:hover { background: #5d3b82; }
            .links { text-align: center; margin-top: 15px; }
            .links a { color: white; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Add Your Business</h1>
            <form method="POST">
                <div class="form-group">
                    <label for="name">Business Name *</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="category">Category *</label>
                    <select id="category" name="category" required>
                        <option value="Local Business">Local Business</option>
                        <option value="Restaurant">Restaurant</option>
                        <option value="Professional Services">Professional Services</option>
                        <option value="Legal">Legal</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="address">Address *</label>
                    <input type="text" id="address" name="address" required>
                </div>
                <div class="form-group">
                    <label for="phone">Phone *</label>
                    <input type="tel" id="phone" name="phone" required>
                </div>
                <button type="submit" class="btn">Add Business</button>
            </form>
        </div>
        <div class="links">
            <a href="/dashboard">Back to Dashboard</a>
        </div>
    </body>
    </html>
    ''')

@app.route('/submit-business/<int:business_id>')
def submit_business(business_id):
    global businesses, submissions
    
    # Find the business
    business = next((b for b in businesses if b.get('id') == business_id), None)
    if not business:
        return "Business not found", 404
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Submit to Directories</title>
        <style>
            body { font-family: Arial; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #333; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            h1, h2 { text-align: center; color: #764ba2; }
            .business { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
            .btn { background: #764ba2; color: white; padding: 12px; border: none; border-radius: 5px; width: 100%; font-size: 16px; cursor: pointer; margin-bottom: 20px; }
            .btn:hover { background: #5d3b82; }
            .progress { height: 20px; background: #eee; border-radius: 10px; margin: 20px 0; overflow: hidden; }
            .progress-bar { height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); width: 0%; transition: width 0.3s; }
            .directory { padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; }
            .results { margin-top: 20px; display: none; text-align: center; }
            .links { text-align: center; margin-top: 15px; }
            .links a { color: white; text-decoration: none; margin: 0 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Submit to Directories</h1>
            <div class="business">
                <p><strong>{{ business.name }}</strong></p>
                <p>{{ business.address }}</p>
                <p>{{ business.phone }}</p>
            </div>
            
            <button id="submit-btn" class="btn" onclick="startSubmission()">Start Submission</button>
            
            <div id="progress-section" style="display:none;">
                <h2>Submission Progress</h2>
                <div class="progress">
                    <div class="progress-bar" id="progress-bar"></div>
                </div>
                <p id="status-text" style="text-align:center;">Preparing submissions...</p>
                
                <div id="directory-list">
                    {% for dir in directories %}
                    <div class="directory">
                        <span>{{ dir.name }}</span>
                        <span id="status-{{ loop.index0 }}">Pending</span>
                    </div>
                    {% endfor %}
                </div>
                
                <div class="results" id="results">
                    <h2>Submission Complete!</h2>
                    <p>Successfully submitted to <span id="success-count">0</span> directories.</p>
                    <a href="/dashboard" style="display: inline-block; background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 20px;">Back to Dashboard</a>
                </div>
            </div>
        </div>
        <div class="links">
            <a href="/dashboard">Back to Dashboard</a>
            <a href="/">Home</a>
        </div>
        
        <script>
            function submitToServer(results) {
                fetch('/api/log-submissions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        business_id: {{ business.id }},
                        results: results
                    })
                });
            }
            
            function startSubmission() {
                document.getElementById('submit-btn').style.display = 'none';
                document.getElementById('progress-section').style.display = 'block';
                
                let directories = {{ directories|tojson }};
                let totalDirectories = directories.length;
                let completedCount = 0;
                let successCount = 0;
                let results = [];
                
                function processDirectory(index) {
                    if (index >= totalDirectories) {
                        // All done
                        document.getElementById('progress-bar').style.width = '100%';
                        document.getElementById('status-text').textContent = 'Completed!';
                        document.getElementById('results').style.display = 'block';
                        document.getElementById('success-count').textContent = successCount;
                        
                        // Log submissions
                        submitToServer(results);
                        return;
                    }
                    
                    let statusElement = document.getElementById(`status-${index}`);
                    statusElement.textContent = 'Processing...';
                    
                    // Simulate submission
                    setTimeout(() => {
                        let success = Math.random() < directories[index].success_rate;
                        
                        if (success) {
                            statusElement.textContent = 'Success';
                            statusElement.style.color = 'green';
                            successCount++;
                            
                            results.push({
                                directory: directories[index].name,
                                status: 'success'
                            });
                        } else {
                            statusElement.textContent = 'Failed';
                            statusElement.style.color = 'red';
                            
                            results.push({
                                directory: directories[index].name,
                                status: 'failed'
                            });
                        }
                        
                        completedCount++;
                        let progress = (completedCount / totalDirectories) * 100;
                        document.getElementById('progress-bar').style.width = `${progress}%`;
                        
                        // Process next directory
                        processDirectory(index + 1);
                    }, 800);
                }
                
                // Start processing
                processDirectory(0);
            }
        </script>
    </body>
    </html>
    ''', business=business, directories=directories)

@app.route('/api/log-submissions', methods=['POST'])
def log_submissions():
    global submissions
    
    data = request.get_json()
    
    business_id = data.get('business_id')
    results = data.get('results', [])
    
    for result in results:
        submission = {
            'id': len(submissions) + 1,
            'business_id': business_id,
            'directory': result.get('directory'),
            'status': result.get('status'),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        submissions.append(submission)
    
    save_data(businesses, submissions)
    return {'status': 'success'}

if __name__ == '__main__':
    app.run(debug=True)
