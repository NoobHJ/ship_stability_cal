# from fastapi import FastAPI
# import uvicorn
# from typing import Union

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "Server"}

# @app.get("/users/{user_id}")
# def get_user(user_id):
#     return {"user_id": user_id}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8000)