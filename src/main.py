from fastapi import FastAPI, Request, HTTPException
import uvicorn


app = FastAPI()


@app.get("/")
def index():
    return {"success": True, "message": "Hello World"}


@app.post("/sms")
def sms(request: Request):
    return {"success": True, "message": "Hello World", "data": request}


if __name__ == "__main__":
    uvicorn.run(app=app, port=8000, host="0.0.0.0")