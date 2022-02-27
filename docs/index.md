# Make US Rich 💰

Welcome, you are at the right place to learn more about the Make US Rich project. 
This project is a tool to help people to train, serve and use cryptocurrencies forecasting models.

<center>
![Money meme](img/money-meme.gif)
<p><em>This is you counting money after deploying the project</em></p>
</center>

This project was build by [@ChainYo](https://github.com/ChainYo) to help people building their own **MLOps projects**.

!!! warning
    Cryptocurrencies are only a pretext to build a **machine learning project**. You won't be able to use this project 
    to make real money, but you can use it to train, serve and use your own models. 

    In fact, you can use the project baselines to train, serve and use **any kind of machine learning models**.

We will see how to use the project in the following sections. Please feel free to ask questions and share your ideas by
[opening an issue](https://github.com/ChainYo/make-us-rich/issues/new). You help and opinion is welcome in order to
improve the project.

## Prerequisites

You need to have a **Python 3.8+** environment to run this project. I personally use `Miniconda` for this purpose.
Combined with `poetry`, it seems to be a good way to manage dependencies and running the project in an isolated
python environment.

- Install [poetry](https://python-poetry.org/docs/)
- Install [Miniconda](https://conda.io/miniconda.html)

The project also requires `docker` and `docker-compose` to be installed. We will use them to run the serving and interface
part of the project.

To install `docker` and `docker-compose` follow the instructions on the [Docker documentation](https://docs.docker.com/install/).

## Installation

Create an isolated python environment with `conda`:

```bash
conda create -y -n make-us-rich python=3.8
```

Activate the environment and install the `make-us-rich` package:

```bash
conda activate make-us-rich
poetry add make-us-rich
```

If you are using pip, you can use the following command instead

```bash
pip install make-us-rich
```

After everything is installed, you can run any component of the project.

## Architecture of the project

The project is composed of three components: `interface`, `serving` and `training`.

Each component has its own folder and its own specific configuration. All details about each component are
explained in their respective documentation.

Here is a simple diagram of the project:

![Project architecture](img/project_architecture.png)

🚀 Let's dive into the components details! 

!!! tip
    *You can start with any, but I recommend to start with the [`training`](/training) component.*
