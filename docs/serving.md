The serving component is the one that will be used to serve models and allow users to make predictions.

It uses the simplicity and rapidity of [FastAPI](https://fastapi.tiangolo.com/) to serve the models.


## Setup

Before we start, you need to check if you are in the right environment. If you are not, follow these 
[instructions](../#installation) to setup the required environment.

Once you have activated your working environment and `make-us-rich` is installed, we are ready to start.

### Initialize the serving component

To **initialize the serving component**, run the following command:

```bash
mkrich init serving
```

This command will create a directory named `mkrich-serving` in your current working directory.

All required files for the serving component will be created in this directory.
Now **navigate** to the directory and open it in your favorite text editor:

```bash
cd mkrich-serving

# I'm using VS Code
code .
```

Don't worry if you don't use **VS Code**, you can open the directory in **any text editor of your choice**.

### Configure the env variables

!!! Success
    If you already have setup Binance API and Object Storage for the training component, you can skip this step and 
    update the env variables files with the same credentials and values you have used for the training component.

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

The only thing you need to do to launch the serving component is to run the following command:

```bash
mkrich run serving
```

This command will start the serving component by building the docker image and running it.

When the serving component is running, you can access it at the following URL: [`http://localhost:8000`](http://localhost:8000).

You should land on the home page which will display the endpoints of the API.