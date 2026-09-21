"""Path Parameters : 
Path parameters are variable segments that form part of the actual URL path. They are typically used to identify a specific, unique resource (like an item ID or username)."""


"""
Query Parameters
Query parameters are key-value pairs that appear after the ? in a URL, separated by &. They are typically used to filter, sort, paginate, or provide optional settings for a collection.
"""

from fastapi import FastAPI, Request
from mockData import products

app = FastAPI()


@app.get("/products")
def get_products():
    return products

# path Param..
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product.get("id") == product_id:
            return product
    return {"error": "Product not found"}


# query param..
@app.get("/greet")
def greet_user(name: str, age: int):
    return f"Hello {name}, and what is your {age}?"



# multiple query param..
@app.get("/greet_user")
def greet_multiple_user(request:Request):
    query_param = dict(request.query_params)
    return f"Hello {query_param.get('name')}, and what is your {query_param.get('age')}?"