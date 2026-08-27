from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return{
        "message": "Hello, welcome to BudolRide Navigator"
    }