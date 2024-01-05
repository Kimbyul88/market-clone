from fastapi import FastAPI,UploadFile,Form,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
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

SECRET = "super-coding"; # 디코딩이 가능해서 숨겨진 정보도 해석할수 있다.
manager = LoginManager(SECRET,'/login.html');
@manager.user_loader()
def query_user(id):
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                        SELECT * from users WHERE id='{id}'
                        """).fetchone() # 하나만 가져올 것이기 때문에!
    return user



@app.post('/login')
def login(id:Annotated[str,Form()], 
           password:Annotated[str,Form()]):
    user = query_user(id)    
    print(user)
    if not user:
        raise InvalidCredentialsException #status에 401을 리턴해준다. 
    elif password != user['password']:
        raise InvalidCredentialsException #200을 리턴해준다.
    
    access_token = manager.create_access_token(data={
        'id':user['id'],
        'name':user['name'],
        'email':user['email']      
    })
    return {'access_token':access_token}

@app.post('/signup')
def signup(id:Annotated[str,Form()], 
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]
           ):
    cur.execute(f"""
                INSERT INTO 
                users(id,name,email,password)
                VALUES ('{id}','{name}','{email}','{password}')  
                """)
    con.commit();
    return '200'

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



app.mount("/", StaticFiles(directory="frontend",html=True), name="frontend")