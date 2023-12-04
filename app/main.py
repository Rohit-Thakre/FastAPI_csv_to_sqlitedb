from fastapi import FastAPI, Request, Form, File, UploadFile,Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import User, SessionLocal

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload/")
async def upload_file(
    request: Request,
    name_column: int = Form(),
    age_column: int = Form(),
    file: UploadFile = File(),
    db: Session = Depends(get_db),
):
    contents = await file.read()


    decoded_contents = contents.decode("utf-8").splitlines()
    csv_data = [line.split(",") for line in decoded_contents]


    # checking data type of before saving to db
    try: 
        int((csv_data[0][age_column-1]))

    except:
        return { "Error msg" : "data type mismatch"}

    try: 

        # reading name and age from csv file
        names = [ row[name_column-1] for row in csv_data]
        ages  = [int(row[age_column-1])  for row in csv_data]

    
        # print("names : ",names)
        # print("ages : ",ages)
    

        # saving data to db
        i = 0
        while(i<len(names)):
            user  = User(name = names[i], age = ages[i] )
            db.add(user)
            i+= 1
        db.commit()

    except IndexError: 
        return {"Error msg" : "Col index of age or name is out of range"}



    message = "File uploaded and data saved to database."
    return {"message": message}
