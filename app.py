from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os, json
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ.get("GOOGLE_CREDS"))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

app = Flask(__name__)

# Connect to Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("DemographicData").sheet1  # MUST match sheet name

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    names = request.form.getlist('name')
    ages = request.form.getlist('age')
    sexes = request.form.getlist('sex')
    addresses = request.form.getlist('address')

    for i in range(len(names)):
        sheet.append_row([names[i], ages[i], sexes[i], addresses[i]])

    return "Saved to Google Sheets!"

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))