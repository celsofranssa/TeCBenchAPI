import uvicorn

from fastapi import FastAPI

from source.entity.Claim import Claim
from source.helper.PredictHelper import PredictHelper

app = FastAPI()
helper = PredictHelper()


@app.get("/")
def read_root():
    return {"I am TecBench-API!"}


@app.post("/predict")
async def predict(claim: Claim):
    return helper.predict(claim)


@app.get('/healthcheck')
def healthcheck():
    return {'healthcheck': 'Everything OK!'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
