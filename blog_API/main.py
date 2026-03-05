from fastapi import FastAPI
from database import create_db_and_tables
from routers import get_routes, other_routes

app = FastAPI()

create_db_and_tables()
 
app.include_router(get_routes.router)
app.include_router(other_routes.router)