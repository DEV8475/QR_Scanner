from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import os

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
file_path = os.path.join(os.path.dirname(__file__), "main-presence-460713-g5-514aee8f3f5b.json")
creds = ServiceAccountCredentials.from_json_keyfile_name(file_path, scope)
client = gspread.authorize(creds)
sheet = client.open("Attendance").sheet1

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        student_id = request.form['student_id'].strip()
        name = request.form['name'].strip()
        today = str(date.today())

        # Read sheet data
        all_data = sheet.get_all_records()
        headers = sheet.row_values(1)

        # Check if student is valid
        found = False
        for row in all_data:
            if str(row["Student ID"]) == student_id and row["Name"].strip().lower() == name.lower():
                found = True
                break

        if not found:
            return render_template("register.html", error="❌ Student not found in record.")

        # Ensure today's column exists
        if today not in headers:
            sheet.update_cell(1, len(headers)+1, today)
            headers.append(today)

        # Find row to mark Present
        for idx, row in enumerate(all_data, start=2):
            if str(row["Student ID"]) == student_id and row["Name"].strip().lower() == name.lower():
                col_index = headers.index(today) + 1
                sheet.update_cell(idx, col_index, "Present")

                # Generate QR URL (external API)
                qr_data = f"{student_id}|{name}"
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={qr_data}"

                return render_template("register.html", success=True, name=name, student_id=student_id, qr_url=qr_url)

    return render_template("register.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)