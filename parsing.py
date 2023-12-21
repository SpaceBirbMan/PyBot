from selenium.webdriver.common.by import By

class TParser:
    url = ""
    driver = None

    def __init__(self, urli: str):
        self.url = urli

    def need_time(self):
            self.driver.get(self.url)

            time_element = self.driver.find_element(By.CSS_SELECTOR, 'div.timeview-data')

            if time_element:
                return time_element.text.strip()
            else:
                return "Information about time not found on the page."


