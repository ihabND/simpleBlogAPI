from fastapi import Depends, APIRouter
from sqlmodel import select
from models import Blog
from database import *

router = APIRouter()

@router.post("/blog") #create new blog
def post_blog(blog: Blog, session: Session = Depends(get_session)):
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog

@router.delete("/blog/{blog_id}") #delete specified blog
def delete_blog(blog_id, session: Session = Depends(get_session)):
    statement = select(Blog).where(Blog.id == blog_id)
    blog = session.exec(statement).first()
    session.delete(blog)
    session.commit()
    return blog

@router.put("/blog/{blog_id}") #update specified blog
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
