
from flask import Flask
import flask
from redis import Redis
import numpy as np
import onnxruntime
from transformers import BertTokenizer

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

# onnxruntime
ort_session = onnxruntime.InferenceSession("resource/onnx/BERTimbau_PROCON.onnx")
input_name = ort_session.get_inputs()[0].name

# text encoding
max_length = 256
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# labels
labels = ['alimentos','combustíveis','finanças','habitação','produtos','publicidade','saúde','serviços públicos e privados','serviços regulamentados pela anatel']

@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')

@app.route('/predict', methods=['POST'])
def predict():
    text = flask.request.get_json(force=True)['text']
    tokenized_text = _encode(text)
    print(tokenized_text.shape)
    print(tokenized_text)
    ort_inputs = {input_name: tokenized_text}
    prediction = ort_session.run(None, ort_inputs)
    
    response = {}

    for label, score in zip(labels, prediction[0].tolist()[0]):
        response[label]=score

    return flask.jsonify(response)

def _encode(text):
    return np.array(
        [tokenizer.encode(text=text, max_length=max_length, padding="max_length", truncation=True)],
        dtype=np.int64
        )
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)