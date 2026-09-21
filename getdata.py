from fastapi import FastAPI

app = FastAPI()

## this is the example of basic FastAPI application with a single endpoint that returns a welcome message. to run this application, save the code in a file named getdata.py and run the command fastapi dev getdata.py then, you can access the endpoint by navigating to http://127.0.0.1:8000/
@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.get("/contact-me")
def contact_me():
    return {"message": "You can contact me at - example@email.com"}