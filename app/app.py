from fastapi import FastAPI

from app.databases.database import init_db, get_session, engine

from app.routers import user, truck, chassis, image_set


app = FastAPI()
app.include_router(user.router)
app.include_router(truck.router)
app.include_router(chassis.router)
app.include_router(image_set.router)
# @app.on_event("startup")
# def on_startup():
#     init_db()




