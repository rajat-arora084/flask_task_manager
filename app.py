from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy, request
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///application.db'
db = SQLAlchemy(app)

class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Task {}, {}, {}>'.format(self.id, self.content, self.date_created.date())


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_content = request.form.get('content')
        print(task_content)
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue with the connection. Please try again'
    else:
        all_tasks = Todo().query.order_by(Todo.date_created).all()
        print(all_tasks)
        return render_template("index.html", tasks=all_tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo().query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an exception deleting the current task {}'.format(id)

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.content = request.form.get('content')
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an exception updating the current task {}'.format(id)
    elif request.method == 'GET':
        return render_template('update.html', task=task_to_update)
    
    

if __name__ == '__main__':
    app.run(debug=True)
