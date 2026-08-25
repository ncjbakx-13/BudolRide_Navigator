from fastapi import FastAPI;

app = FastAPI();

@app.get("/")
def root():
    return {"message": "Welcome to BudolRide Navigator"}

@app.get("/choose-route")
def chooseRoute():
    return {"message": "Choose your route"}

@app.get("/stores/{store_id}")
def getStore(store_id: int):
    return {"id": 123,
            "name": "nathaniel brax"}