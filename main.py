from fastapi import FastAPI

app = FastAPI()


@app.get("/bitch")
async def hello_world_bitch():
    return {"HEELLO": "MTHRFCKR"}


if __name__ == "__main__":
    print("Server starts")
