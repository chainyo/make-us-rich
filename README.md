# 🚧 Be carefull this repo is still a work in progress

What is already functional?
- [ ] Prefect Flows - 80%
- [x] Training pipeline - 100%
- [x] Serving models - 100%
- [x] Interface - 100%
- [ ] CLI - 70%
- [ ] Documentation - 0%

Dev package available on [PyPI](https://pypi.org/project/make-us-rich/).

# Make Us Rich
Deep Learning applied to cryptocurrency forecasting.

For more details on how to use this project, please refer to [documentation](https://chainyo.github.io/make-us-rich/).

You can inspect the training pipeline with the `Kedro Viz` tool, available [here](https://makeusrich-viz.chainyo.tech)

---

## Introduction

We provide a simple way to train, serve and use cryptocurrency forecasting models on a daily basis.

![Project Architecture](assets/project_architecture.png)

Every hour `Prefect` flows are launched to train and store models automatically.
Each flow has 2 variables: `currency` and `compare` to identify which type of data the `fetching data` part
needs to get from the `Binance API` to train the model.

For example, if you want to train a model on the currency `Bitcoin` compared with `US Dollar`: `currency="btc",compare="usdt"`.

You have to give the symbol for each variable. Find all available symbols on the 
[Binance](https://www.binance.com/en/markets) platform.

Once the `Kedro` pipeline is launched, everything works smoothly and automatically. 

There is 5 steps for the pipeline to complete:
- 🪙 Fetching data from Binance API.
- 🔨 Preprocessing data:
    - Extract features from fetched data.
    - Split extracted features.
    - Scale splitted features.
    - Create sequences with scaled train features.
    - Create sequences with scaled test features.
    - Split train sequences as train and validation sequences.
- 🏋️ Training model.
- 🔄 Converting model to ONNX format.
- 📁 Uploading converted model to object storage service.

After the end of the training pipeline, the new model will be available for serving. 
Every 10 minutes, a `Prefect` flow is launched to update the API with lastest available models for each currency.

The final step is the crypto dashboard that allows users to see forecasting for their favorite assets.

---

## Prerequisites

The main project has `poetry` as package manager. If you need to install poetry, check their awesome 
[documentation](https://python-poetry.org/docs/).

You don't need to clone this project to your local machine. You can simply install the `make-us-rich` package with this 
command:
```bash
$ pip install make-us-rich
```

It's recommended to have an isolated environment for each component of the project, unless you run everything on the 
same machine.


## CLI Usage

TODO
