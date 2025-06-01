from fastapi import FastAPI

app = FastAPI()

app.get("/")


def home():
    return "<h1>Hello world</h1>"
