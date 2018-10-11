from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g
##from flask-login import login_user , logout_user , current_user , login_required

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def main():
    return render_template('index.html')

##@app.route('/login', methods=['GET', 'POST'])
##  def login():
##    error = None
##    if request.method == 'GET':
##        return render_template('index.html')
##    username = request.form['username']
##    password = request.form['password']
##    registered_user = User.query.filter_by(username=username,password=password).first()
##    if registered_user = None:
##        flash('Username or Password is invalid', 'error')
##        return redirect(url_for('login'))
##    login_user(registered_user)
##    flash('Logged in successfuly')
##    return redirect(request.args.get('next') or url_for('index'))

if __name__ == "__main__":
    app.run()