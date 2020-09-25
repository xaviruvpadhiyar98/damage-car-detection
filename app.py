from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from glob import glob
from modelpredict import ModelPredict
from os import remove

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

files_to_remove = []


@app.get("/")
async def root(request: Request):
    print(files_to_remove)
    try:    
        for x in files_to_remove:
            remove(x)
            files_to_remove.remove(x)
    except Exception as e:
        print(e)
    return templates.TemplateResponse("index.html", {
        'request': request,
    })

@app.post("/predict/")
async def create_upload_files(request: Request,file: UploadFile = File(...)):
    if 'image' in file.content_type:
        contents = await file.read()
        filename = 'static/' + file.filename
        with open(filename, 'wb') as f:
            f.write(contents)
        m = ModelPredict(filename).predict()
        files_to_remove.append(filename) 

        return templates.TemplateResponse("predict.html", {
            "request": request,
            "filename": file.filename,
            "Predict": m
        })
    else:
        return {"Error":'Not a Valid File - Please Upload Image Of Damage Area of Car'}


