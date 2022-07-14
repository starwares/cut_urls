from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sql:1111@127.0.0.1:5432/cat_urls'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return '<Urls %r>' % self.id


@app.route("/<int:some_id>/")
def redir(some_id):
    urls = Urls.query.all()
    for i in urls:
        if i.id == some_id:
            return redirect(i.url)
    return "Такого адреса нет, перепроверьте введенные данные"


@app.route("/all_url")
def all_url():
    urls = Urls.query.order_by(Urls.id.desc()).all()
    return render_template("all_url.html", urls=urls)


@app.route("/", methods=['POST', 'GET'])
def run_code():
    if request.method == 'POST':
        url = request.form['url']
        urls = Urls(url=url)
        try:
            db.session.add(urls)
            db.session.commit()
            return render_template("new_url.html", id=urls.id)
        except:
            return "При добавлении URL возникла ошибка"
    else:
        return render_template("index.html")




if __name__ == '__main__':
    app.run(debug=True)