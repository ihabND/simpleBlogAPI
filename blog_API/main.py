from fastapi import Depends, FastAPI
from sqlmodel import select
from models import Blog
from database import *

app = FastAPI()

create_db_and_tables()
    
@app.get("/")
def get_root():
    return {"Welcome" : "Home Page"}

@app.get("/blog") #all or by category
def get_blogs(category = None, session: Session = Depends(get_session)):
    if category:
        statement = select(Blog).where(Blog.category == category)
    else:
        statement = select(Blog)
    blogs = session.exec(statement).all()
    #print(type(blogs))
    return blogs

@app.get("/blog/{blog_id}") #by specified id
def get_blog(blog_id, session: Session = Depends(get_session)):
    statement = select(Blog).where(Blog.id == blog_id)
    blog = session.exec(statement).first()
    #print(type(blog))
    return blog

@app.post("/blog") #create new blog
def post_blog(blog: Blog, session: Session = Depends(get_session)):
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog

@app.delete("/blog/{blog_id}") #delete specified blog
def delete_blog(blog_id, session: Session = Depends(get_session)):
    statement = select(Blog).where(Blog.id == blog_id)
    blog = session.exec(statement).first()
    session.delete(blog)
    session.commit()
    return blog

@app.put("/blog/{blog_id}") #update specified blog
def update_blog(blog_id, new_data: Blog, session: Session = Depends(get_session)):
    statement = select(Blog).where(Blog.id == blog_id)
    blog = session.exec(statement).first()
    blog.title = new_data.title
    blog.content = new_data.content
    blog.category = new_data.category
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog

@app.get("/search") #search titles and contents by a term
def search_blogs(term, session: Session = Depends(get_session)):
    found_blogs = []
    term = term.lower()
    statement = select(Blog)
    blogs = session.exec(statement).all()
    for blog in blogs:
        if(term in blog.title.lower() or term in blog.content.lower()):
            blog.title = blog.title.lower().replace(term, term.upper())
            blog.content = blog.content.replace(term, term.upper())
            found_blogs.append(blog)
    if found_blogs:
        return found_blogs
    else:
        return {"No results"}


