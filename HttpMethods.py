from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from mockData import products

app = FastAPI()

class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


class ProductUpdate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


class ProductPatch(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None


# 1. GET (Read) - Safe & Idempotent
@app.get("/products", status_code=status.HTTP_200_OK)
def get_products():
    return products


@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
def get_product(product_id: int):
    for product in products:
        if product.get("id") == product_id:
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )


# 2. POST (Create)
# Submits data to create a new resource.
# NOT safe, NOT idempotent (submitting twice creates duplicate items).
@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    # Generate a new ID based on the max ID or length
    new_id = max([p["id"] for p in products], default=0) + 1
    new_product = {"id": new_id, **product.model_dump()}
    products.append(new_product)
    return new_product


# 3. PUT (Full Update / Replace)
# Replaces the entire target resource with the uploaded payload.
# NOT safe, IDEMPOTENT (calling it multiple times with the same data yields the same state).
@app.put("/products/{product_id}", status_code=status.HTTP_200_OK)
def update_product(product_id: int, updated_data: ProductUpdate):
    for index, product in enumerate(products):
        if product.get("id") == product_id:
            # Complete replacement of fields while preserving the ID
            replaced_product = {"id": product_id, **updated_data.model_dump()}
            products[index] = replaced_product
            return replaced_product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )


# 4. PATCH (Partial Update)
# Applies partial modifications to a resource. Only the provided fields are updated.
# NOT safe, NOT strictly idempotent by spec (though often idempotent in practice)
@app.patch("/products/{product_id}", status_code=status.HTTP_200_OK)
def patch_product(product_id: int, patch_data: ProductPatch):
    for product in products:
        if product.get("id") == product_id:
            # exclude_unset=True ignores fields that were not provided in the request
            update_dict = patch_data.model_dump(exclude_unset=True)
            product.update(update_dict)
            return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )

# 5. DELETE (Remove)
# Deletes the specified resource.
# NOT safe, IDEMPOTENT (deleting an already deleted resource results in the resource staying deleted).
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product.get("id") == product_id:
            products.pop(index)
            return None

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )