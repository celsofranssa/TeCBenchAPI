# TeCBenchAPI - Classificador de Manifestações do ProconData.

RESTful API para classificar textos de manifestações.

## Building
```
# build a docker image for TeCBenchAPI
docker build -t tecbench-api .
```

## Deploying
```
docker run -p 8000:8000 tecbench-api
```
    

## Endpoints:

### /predict

* Tipo de requisição: POST
* Corpo da requisição:

```
    {
        "idx": 25,
        "text": "o o site nao entregou a mercadoria"
    }
```

### Resposta:
```
{
    "alimentos": 0.010813464410603046,
    "combustíveis": 0.008098076097667217,
    "finanças": 0.05324026942253113,
    "habitação": 0.013248320668935776,
    "produtos": 0.3358003795146942,
    "publicidade": 0.09058813005685806,
    "saúde": 0.014323397539556026,
    "serviços públicos e privados": 0.43174874782562256,
    "serviços regulamentados pela anatel": 0.042139168828725815
}
```

