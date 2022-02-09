# Make Us Rich

We were using `Celery` to run tasks in the background, but it's now deprecated in favor of `Prefect`.

You can see `Prefect` flow initialization code in the 
[`src/trainer/register_prefect_flow.py`](../trainer/register_prefect_flow.py) file.

## Prefect commands

Install `Prefect` with `pip install prefect`.

By default, `Prefect` will use `Prefect Cloud` as the backend. So after installing `Prefect`, 
you need run the following command to use `Prefect Server` as backend:

```bash
$ prefect backend server
```

Now you can start the server using the command:

```bash
$ prefect server start
```
