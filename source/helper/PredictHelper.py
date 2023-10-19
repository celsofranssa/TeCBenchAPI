from datetime import time

import numpy as np
import onnxruntime
from transformers import BertTokenizer, AutoTokenizer
from scipy.special import softmax


class PredictHelper:

    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.labels = ['publicidade', 'serviços regulamentados pela anatel', 'finanças', 'produtos', 'extra-procon', 'serviços públicos e privados', 'serviço de atendimento ao consumidor', 'criminal', 'alimentos', 'saúde', 'combustíveis', 'habitação', 'administrativo – institucional']

        self._load_onnxruntime()

    def _load_onnxruntime(self):
        # onnxruntime
        self.ort_session = onnxruntime.InferenceSession(
            "resource/onnx/TeCBench_MPMG_VRS_1.0.0.onnx",
            providers=["CPUExecutionProvider", "CUDAExecutionProvider"]
        )
        self.input_name = self.ort_session.get_inputs()[0].name

    def _get_tokenizer(self, params):
        return AutoTokenizer.from_pretrained(
            params.architecture
        )

    def _encode(self, text):
        return np.array(
            [self.tokenizer.encode(text=text, max_length=256, padding="max_length", truncation=True)],
            dtype=np.int64
        )

    def predict(self, claim):
        # tokenizing text
        tokenized_text = self._encode(claim.text)

        # defining inputs
        ort_inputs = {self.input_name: tokenized_text}

        # predicting and reshaping
        prediction = self.ort_session.run(None, ort_inputs)
        return self._reshape_prediction(prediction)

    def _reshape_prediction(self, prediction):
        reshaped_prediction = {}
        for label, score in zip(self.labels, softmax(prediction[1].tolist()[0])):
            reshaped_prediction[label] = score
        return reshaped_prediction
