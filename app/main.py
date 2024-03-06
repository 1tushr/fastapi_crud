from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database_config import DATABASE_CONFIG
from .models import Post

# Create a FastAPI instance
app = FastAPI()

# Database connection setup
while True:
    try:
        conn = psycopg2.connect(
            host=DATABASE_CONFIG["host"],
            dbname=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Error in connecting to the database")
        print("Error:", error)
        time.sleep(2)


# Route to get all posts
@app.get("/posts")
async def get_post():
    try:
        # Execute SQL query to select all posts
        cursor.execute("""SELECT * FROM posts""")
        # Fetch all records
        products = cursor.fetchall()
        print(products)
        return {"databases": products}
    except Exception as error:
        print("Error:", error)


# Route to create a new post
@app.post("/newpost")
async def new_post(post: Post):
    try:
        # Execute SQL query to insert a new post
        cursor.execute(
            """INSERT INTO posts (title, content, published) VALUES (%s,%s, %s) RETURNING * """,
            (post.title, post.content, post.published),
        )
        # Fetch the newly inserted post
        new_post = cursor.fetchone()
        conn.commit()
        return {"data": new_post}
    except Exception as error:
        print("Error:", error)


# Route to get a specific post by ID
@app.get("/fetchpost/{id}")
async def get_one_post(id: int):
    try:
        # Execute SQL query to select a post by ID
        cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
        # Fetch the record
        post_found = cursor.fetchall()
        return {"data": post_found}
    except Exception as error:
        print("Error:", error)


# Route to edit/update a post by ID
@app.put("/editpost/{id}")
async def edit_post(id: int, post: Post):
    try:
        # Execute SQL query to update a post by ID
        cursor.execute(
            """ UPDATE posts SET title= %s, content=%s, published=%s WHERE id = %s RETURNING *""",
            (post.title, post.content, post.published, str(id)),
        )
        # Fetch the updated post
        updated_post = cursor.fetchone()
        conn.commit()
        return {"details": updated_post}
    except Exception as error:
        print("Error:", error)


# Route to delete a post by ID
@app.delete("/deletepost/{id}")
async def delete_post(id: int):
    try:
        # Execute SQL query to delete a post by ID
        cursor.execute(
            """DELETE FROM posts WHERE id = %s RETURNING *""",
            (str(id),),
        )
        # Fetch the deleted post
        deleted_post = cursor.fetchone()
        conn.commit()
        return {"details": deleted_post}
    except Exception as error:
        print("Error:", error)


# Root route
@app.get("/")
async def root():
    return {"message": "Hello, this is FastAPI"}
