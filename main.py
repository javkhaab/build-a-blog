from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://build-a-blog:11230809@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True


db = SQLAlchemy(app)


class  Blog(db.Model):
       id = db.Column(db.Integer, primary_key= True)
       title = db.Column(db.String(120))
       body = db.Column(db.String(600))

       def __init__(self, title, body):
          self.title = title
          self.body = body
blogs=[]

@app.route('/')
def index():
    blogs=Blog.query.order_by("id").all()
    return render_template('index.html',title='Build a Blog!',blogs=blogs)



@app.route('/blog')
def blog():
    blogid= request.args.get('id')
    if request.method=='GET':
        if not request.args.get('id') is None:
            
            singleid=Blog.query.get(int(blogid))
            return render_template('single.html',title='Single Post!',blogs=singleid)
    blogs=Blog.query.order_by("id desc").all()  
    return render_template('blog.html',title='Build a Blog!',blogs=blogs)




@app.route('/newpost',methods=['POST', 'GET'])
def submitpost():

    if request.method=='GET':
        return render_template('post.html',title='Build a Blog!')


    
    else :
        title = request.form['title']
        body = request.form['body']
        if title=="" or body=="":
            flash("it should not be empty")
            return render_template('post.html')
    
        newpost=Blog(title,body)
        db.session.add(newpost)
        db.session.commit()
        id = str(newpost.id)
        return redirect("/blog?id=" + id)
     


    return render_template('post.html',title='Build a Blog!')
    
    
    
 

if __name__=='__main__':
    app.run()