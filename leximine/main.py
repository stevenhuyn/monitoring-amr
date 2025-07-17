import json


def main():
    print("Hello from leximine!")
    readConfig()


def readConfig():
    with open("config.json", "r") as f:
        config = json.load(f)

    print(config)


if __name__ == "__main__":
    main()
