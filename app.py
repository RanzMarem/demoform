from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os, json
from datetime import datetime

app = Flask(__name__)

# --- Google Sheets setup (Render-safe) ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Read credentials from environment variable
creds_dict = json.loads(os.environ["GOOGLE_CREDS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)
sheet = client.open("DemographicData").sheet1  # EXACT sheet name

# --- Routes ---
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    names = request.form.getlist('name')
    ages = request.form.getlist('age')
    sexes = request.form.getlist('sex')
    addresses = request.form.getlist('address')

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for i in range(len(names)):
        sheet.append_row([timestamp, names[i], ages[i], sexes[i], addresses[i]])

    # Redirect back to form with a query parameter to show success message
    return redirect(url_for('index', success=1))

# --- Optional: show success popup in HTML ---
# In your index.html, you can check for the query parameter `success=1` and display a message

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))