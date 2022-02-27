The training component is the one that will be used to automatically schedule and launch training jobs.

To automate the training process, we will use `Prefect` to schedule and run the training jobs and `Kedro` that handles 
the different steps represented as modular pipelines.

## Setup

Before we start, you need to check if you are in the right environment. If you are not, follow these 
[instructions](../#installation) to setup the required environment.

Once you have activated your working environment and `make-us-rich` is installed, we are ready to start.


### Initialize the training component

To **initialize the training component**, run the following command:

```bash
mkrich init training
```

This command will create a directory named `mkrich-training` in your current working directory.

All required files for the training component will be created in this directory.   
Now **navigate** to the directory and open it in your favorite text editor:

```bash
cd mkrich-training

# I'm using VS Code
code .
```

Don't worry if you don't use **VS Code**, you can open the directory in **any text editor of your choice**.


### Configure the env variables

#### Binance API

The training component requires some environment variables to be set. 

This component uses the `Binance` exchange API to fetch the required data. You can easily create an account on `Binance`
by following the [instructions](https://www.binance.com/en/register) and then get your API key and secret.

When your binance account is created, you will be able to access the API key and secret in your account settings. Please
follow these [FAQ instructions](https://www.binance.com/en/support/faq/360002502072) to get your API key and secret.

!!! warning
    Never share your API key and secret with anyone. I recommend to create an `read-only` API key and secret, in order
    to avoid any security risk. `read-only` means that you cannot trade with the API key and secret.

Creating and validating your account could take a while. Please be patient, it's worth it. After everything is done,
the access to the `Binance` API will be immediately available.

Once you have your API key and secret, you can set them as environment variables in the dedicated env file located
in `/mkrich-training/conf/base/.env-binance`.

!!! info
    To avoid credentials exposure, a .gitignore file is created during the initialization process to exclude  the `conf/`
    folder from the git repository.

#### Object Storage

In this project we will use **Minio** as object storage. You can use any other object storage service, but Minio is a
good choice, because it is easy to use and it is free. You can use **AWS S3** or **Azure** as well because they are
all compatible with Minio.

Because running an object storage service is out of the scope of this project, we won't describe how to set up the
service here and assume you already have it.

!!! note
    If you don't have any object storage service, check online ressources and you will find a lot of tutorials.

    Finally, if you don't succeed, you still can open an issue on the make-us-rich repository to ask for help. Maybe,
    I will be able to help you to set up your object storage service 🤗.

When you have your object storage service ready, you can change all required env variables in the env file located
in `/mkrich-training/conf/base/.env-minio`.

`ACCESS_KEY` and `SECRET_KEY` are the credentials to access your object storage service. I recommend to create an 
dedicated user for this purpose, with limited permissions.     
The user only needs to upload and download files in the bucket you defined as `BUCKET` in the env file. The `ENDPOINT` 
is the URL of your object storage service used to interact with it.


## Launch

There is two steps to make the training component fully functional.

### Setup Prefect

[Prefect](https://www.prefect.io/) is an usefull tool to automating and monitoring the execution of tasks. 
We will use this great tool combined with `Kedro` to automate the training process. 

[Kedro](https://kedro.readthedocs.io/en/stable/) is a Python framework that allows to build modular pipelines.

Because I already configured everything for you, you can launch the training component by running the following command:

```bash
mkrich run training
```

!!! tip
    Be sure to be in the `mkrich-training` directory before running the command.

When the training component is launched, you will get access to a nice dashboard that will show you the status of 
**registered flows**. A `flow` is a set of tasks that will be executed in sequence by a Prefect worker, also known as 
an **agent**.

By default, the dashboard is available at [`http://127.0.0.1:8080`](http://127.0.0.1:8080/default). You can navigate to
the [flows tab](http://127.0.0.1:8080/default?flows) to see the registered flows. If everything is working, you should
see three different flows: `btc_usdt`, `eth_usdt` and `chz_usdt` which belongs to the `make-us-rich` project.

All registered flows are scheduled to run every hour by default. You can change this behavior by editing the `schedule`
of each flow. 

For the moment, no flow is running because `Prefect` needs an available agent to run the flows. So let's create a 
worker to run the flows.

### Create a local agent

To create a local agent, you need to run the following command:

```bash
mkrich start agent
```

This will start a local agent that will run the registered flows in parallel in the background.

If you don't want to run a local agent, you can refer to the [Prefect documentation](https://www.prefect.io/docs/agent/start)
to create a remote agent or an agent in a Docker container.

### Stop the training component

You can simply stop the agent by closing the terminal where you started it.

To stop all the training component, run the following command:

```bash
mkrich stop
```

This command will stop all containers launched by `Prefect` and remove them.


## Training pipeline

### Steps of the training pipeline

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

Once all the steps are completed, you will have a trained model ready to be used and available in the object storage.

Models are used by the [serving](../serving) component to make predictions.

### Training parameters

You can change the training parameters by editing the dedicated file located in `/mkrich-training/conf/base/parameters.yml`.

#### GPU or CPU

The `run_on_gpu` parameter defines if the training will be done on a GPU or not. Set it to `True` if you have a GPU and 
you want to use it for training, otherwise set it to `False`.

#### WandB logging

The training pipeline will log the training process to [WandB](https://wandb.ai/site).

You will need to create an account on [WandB](https://wandb.com/login) in order to use this feature. It's free for a 
personal user and you can create as many projects as you want.

Once registered, you need to [authenticate](https://docs.wandb.ai/quickstart#1.-set-up-wandb) though the `wandb` cli tool. 
You can do it by running the following command:

```bash
wandb login
```

Don't forget to change the `wandb_project` parameter in the `parameters.yml` file if you want to use a different name
for your project.

!!! tip
    PyTorch Lightning has a [WandB integration](https://pytorch-lightning.readthedocs.io/en/latest/common/loggers.html#weights-and-biases) 
    feature which allows us to automatically log all the training process to the WandB platform.


## Find help

If you need help to understand or to use the training component, please open an issue on the 
[make-us-rich repository](https://github.com/ChainYo/make-us-rich/issues). I will be able to help you!
