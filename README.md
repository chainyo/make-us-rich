# 🚧 Be carefull this repo is still a work in progress

What is already functional?
- [ ] Cron jobs - 0%
- [ ] Workers - 80%
- [x] Training pipeline - 100%
- [ ] Serving models - 10%
- [ ] Interface - 50%

# Make Us Rich
Deep Learning applied to cryptocurrency forecasting.

For more details about this project, please refer to [documentation](/docs). (⚠️ Not ended yet.)

You can also access to [Kedro Visualization](https://kedro.readthedocs.io/en/stable/03_tutorial/06_visualise_pipeline.html) tool in order to inspect in details the [full training pipeline]().

---

## Introduction

We provide a simple way to train, serve and use cryptocurrency forecasting models on a daily basis.

![Project Architecture](docs/assets/project_architecture.png)

Every day `cron` jobs send to `celery` workers the order to launch multiples training pipelines.
Each order contains 2 variables: `currency` and `compare` to identify which type of data the `fetching data` part
needs to get.

For example, if you want to train a model on the currency `Bitcoin` compared with `US Dollar` the `cron` jobs will give: `currency="btc",compare="usdt"`.

You have to give the symbol for each variable. Find all available symbols on the 
[Binance](https://www.binance.com/en/markets) platform.

One `celery` worker will launch a pipeline with these 2 values. Once the pipeline is
launched, everything works smoothly and automatically. 

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

After the end of the training pipeline, the new model will be loaded on the serving server where it could be consumed via API.

The final step is the crypto dashboard that allows users to see forecasting for their favorite assets.

---

## How to use it

This is the project repository architecture:

```
📦src
 ┣ 📂serving
 ┃ ┗...
 ┣ 📂interface
 ┃ ┗...
 ┣ 📂trainer
 ┃ ┗...
 ┗ 📂worker
   ┗...
```
