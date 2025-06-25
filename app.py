from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']

        # Combine data and generate QR API link
        qr_data = f"{student_id}|{name}"
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={qr_data}"

        return render_template('register.html', qr_url=qr_url, name=name, student_id=student_id)

    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)