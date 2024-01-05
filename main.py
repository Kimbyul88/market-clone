from fastapi import FastAPI,UploadFile,Form,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect('dbdb.db',check_same_thread=False)
cur = con.cursor()

cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items(
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                image BLOB,
                price INTEGER NOT NULL,
                description TEXT,
                place TEXT NOT NULL,
                insertAt INTEGER NOT NULL
            );
            """)

app = FastAPI()

@app.post("/items")
async def create_item(
                image:UploadFile, 
                title:Annotated[str,Form()], 
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
                ):

    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO 
                items(title,image,price,description,place,insertAt)
                VALUES ('{title}','{image_bytes.hex()}',{price},'{description}','{place}',{insertAt})    
                """)
    con.commit()
    return '200'

@app.get("/items") # items라는 get요청이 들어왔을때!
async def get_items():
    #컬럼명도 같이 가져옴
    con.row_factory = sqlite3.Row
    cur = con.cursor() #db에서 현재 커넥션의 위치를 업데이트 해준다.
    rows = cur.execute(f"""
                        SELECT * from items;
                        """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))

@app.get("/images/{item_id}")
async def get_image(item_id):
    cur = con.cursor()
    #16진법
    image_bytes = cur.execute(f"""
                             SELECT image from items WHERE id={item_id}
                             """).fetchone()[0]
    return Response(content=bytes.fromhex(image_bytes),media_type='image/*')
#image_bytes는 16진법, bytes.fromhex()는 괄호안을 2진법으로 바꿔줌. 

@app.post('/signup')
def signup(id:Annotated[str,Form()], password:Annotated[str,Form()]):
    print(id,password)
    return '200'

app.mount("/", StaticFiles(directory="frontend",html=True), name="frontend")