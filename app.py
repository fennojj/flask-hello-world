from flask import Flask, render_template_string, request, redirect, url_for
import time
import random

app = Flask(__name__)

# Simple data storage
businesses = []
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
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/add-business', methods=['GET', 'POST'])
def add_business():
    if request.method == 'POST':
        business = {
            'id': len(businesses) + 1,
            'name': request.form['name'],
            'category': request.form['category'],
            'address': request.form['address'],
            'phone': request.form['phone']
        }
        businesses.append(business)
        return redirect(url_for('submit_business', business_id=business['id']))
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Business</title>
        <style>
            body { font-family: Arial; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #333; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; }
            h1 { text-align: center; margin-bottom: 30px; color: #764ba2; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; }
            input, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            .btn { background: #764ba2; color: white; padding: 12px; border: none; border-radius: 5px; width: 100%; font-size: 16px; cursor: pointer; }
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
    </body>
    </html>
    ''')

@app.route('/submit-business/<int:business_id>')
def submit_business(business_id):
    business = next((b for b in businesses if b['id'] == business_id), None)
    if not business:
        return "Business not found", 404
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Submit to Directories</title>
        <style>
            body { font-family: Arial; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #333; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; }
            h1, h2 { text-align: center; color: #764ba2; }
            .business { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
            .btn { background: #764ba2; color: white; padding: 12px; border: none; border-radius: 5px; width: 100%; font-size: 16px; cursor: pointer; }
            .progress { height: 20px; background: #eee; border-radius: 10px; margin: 20px 0; overflow: hidden; }
            .progress-bar { height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); width: 0%; transition: width 0.3s; }
            .directory { padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; }
            .results { margin-top: 20px; display: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Submit to Directories</h1>
            <div class="business">
                <p><strong>{{ business.name }}</strong></p>
                <p>{{ business.address }}</p>
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
                </div>
            </div>
        </div>
        
        <script>
            function startSubmission() {
                document.getElementById('submit-btn').style.display = 'none';
                document.getElementById('progress-section').style.display = 'block';
                
                let totalDirectories = {{ directories|length }};
                let completedCount = 0;
                let successCount = 0;
                
                function processDirectory(index) {
                    if (index >= totalDirectories) {
                        // All done
                        document.getElementById('progress-bar').style.width = '100%';
                        document.getElementById('status-text').textContent = 'Completed!';
                        document.getElementById('results').style.display = 'block';
                        document.getElementById('success-count').textContent = successCount;
                        return;
                    }
                    
                    let statusElement = document.getElementById(`status-${index}`);
                    statusElement.textContent = 'Processing...';
                    
                    // Simulate submission
                    setTimeout(() => {
                        let success = Math.random() < {{ directories[index].success_rate }};
                        
                        if (success) {
                            statusElement.textContent = 'Success';
                            statusElement.style.color = 'green';
                            successCount++;
                        } else {
                            statusElement.textContent = 'Failed';
                            statusElement.style.color = 'red';
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

if __name__ == '__main__':
    app.run(debug=True)
