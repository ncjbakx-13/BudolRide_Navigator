from fastapi import FastAPI, Body

app = FastAPI()

account = [
    {
        "id": 100,
        "username": "aaronangat",
        "totalRide": 3,
        "isOnline": True
    },
    {
        "id": 101,
        "username": "nathbakx",
        "totalRide": 15,
        "isOnline": False
    },
    {
        "id": 102,
        "username": "johnrev",
        "totalRide": 10,
        "isOnline": True
    }

]

@app.get("/")
def root():
    return{
        "message": "Hello, welcome to BudolRide Navigator"
    }

@app.get("/login")
def login():
    return{
        "message": "Please login your account"
    }

@app.get("/api/account")
def get_account(totalRide:int | None = None):
    if totalRide is None:
        return account
    
    result=[]
    for user in account:
        if user["totalRide"] >= totalRide :
            result.append(user)
    return result

@app.post("/api/account")
def create_account(new_account=Body()):
    account.append(new_account)
    return{
        "message": "Account created successfully",
        "account": new_account
    }
