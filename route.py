from flask import Flask, render_template

app = Flask(__name__)

@app.route('/create-anggota')
def create_anggota():
    return render_template('create-anggota.html')

@app.route('/create-hobi')
def create_hobi():
    return render_template('create-hobi.html')

@app.route('/select-hobi')
def select_hobi():
    return render_template('select-hobi.html')

@app.route('/show-anggota')
def show_anggota():
    return render_template('show-anggota.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
