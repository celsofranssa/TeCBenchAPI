import numpy as np
import onnxruntime
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
from transformers import BertTokenizer

# Create an object of class FastAPI
global app
app = FastAPI()

ort_session = onnxruntime.InferenceSession("resource/onnx/BERTimbau_PROCON.onnx")
input_name = ort_session.get_inputs()[0].name

max_length = 256
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")


def _encode(sample):
    tokenized_sample = tokenizer.encode(text=sample["text"], max_length=max_length, padding="max_length",
                                        truncation=True),
    return np.array(tokenized_sample, dtype=np.int64)

labels = ['alimentos','combustíveis','finanças','habitação','produtos','publicidade','saúde','serviços públicos e privados','serviços regulamentados pela anatel']
class Data(BaseModel):
    """In fast-api this class is created just for documentation purposes"""
    text: str


@app.post("/predict")
def predict(sample: Data):
    sample = sample.dict()
    print(sample)
    #
    tokenized_sample = _encode(sample)
    print(tokenized_sample.shape)
    print(tokenized_sample)
    # prediction = ort_session.run(None, tokenized_sample)

    #ort_session = onnxruntime.InferenceSession("resource/onnx/BERTimbau_PROCON.onnx")
    #input_name = ort_session.get_inputs()[0].name
    ort_inputs = {input_name: tokenized_sample}
    prediction = ort_session.run(None, ort_inputs)

    response = {}
    for label, score in zip(labels, prediction[0].tolist()[0]):
        response[label]=score

    print(f"Prediction: {prediction}")

    return {"prediction": str(response)}
# def predict(sample: Data):
#     sample = sample.dict()
#     print(sample)
#     try:
#         tokenized_sample = _encode(sample)
#         print(tokenized_sample.shape)
#         print(tokenized_sample)
#         prediction = ort_session.run(None, tokenized_sample)
#
#         return {"prediction": prediction}
#     except:
#         return {"prediction": "error"}
