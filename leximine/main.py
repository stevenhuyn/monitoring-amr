import tomllib
from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    print("Hello from leximine!")
    readConfig()
    seleniumHello()


def readConfig():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    print(config)


def seleniumHello():
    driver = webdriver.Chrome()

    driver.get("https://selenium.dev/documentation")
    assert "Selenium" in driver.title

    elem = driver.find_element(By.ID, "m-documentationwebdriver")
    elem.click()
    assert "WebDriver" in driver.title

    print(elem)


if __name__ == "__main__":
    main()
