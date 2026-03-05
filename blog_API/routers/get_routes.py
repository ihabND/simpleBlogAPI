from fastapi import Depends, APIRouter
from sqlmodel import select
from models import Blog
from database import *

router = APIRouter()

@router.get("/")
def get_root():
    return {"Welcome" : "Home Page"}

@router.get("/blog") #all or by category
def get_blogs(category = None, session: Session = Depends(get_session)):
    if category:
        statement = select(Blog).where(Blog.category == category)
    else:
        statement = select(Blog)
    blogs = session.exec(statement).all()
    #print(type(blogs))
    return blogs

@router.get("/blog/{blog_id}") #by specified id
def get_blog(blog_id, session: Session = Depends(get_session)):
    statement = select(Blog).where(Blog.id == blog_id)
    blog = session.exec(statement).first()
    #print(type(blog))
    return blog

@router.get("/search") #search titles and contents by a term
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