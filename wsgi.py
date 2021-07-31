from flask import render_template
from app import create_app

app = create_app()

@app.errorhandler(400)
def error_400(error):
    return render_template('errors/400.html'), 400

@app.errorhandler(401)
def error_401(error):
    return render_template('errors/401.html'), 401

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)