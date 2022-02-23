from make_us_rich.worker import Trainer


if __name__ == "__main__":
    flow = Trainer()
    print(flow.list_registered_flows())