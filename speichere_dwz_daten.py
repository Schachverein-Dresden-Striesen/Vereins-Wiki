# Generated by Selenium IDE
# https://applitools.com/tutorials/selenium-ide.html#selenium-ide-videos
# https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-win64.zip

import logging
import os
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s:%(name)s:%(message)s"
)
LOGGER = logging.getLogger()
LOGGER.addHandler(logging.FileHandler(f"{__file__}.log"))
logging.getLogger("selenium").setLevel(logging.INFO)
logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)

basename = "F2810_DWZ".lower()

PAT_HEADERS = ".//thead/tr/th"
PAT_ROWS = ".//tbody/tr"
PAT_CELLS = ".//td"

URL_LOGIN = "https://www.schachbund.de/anmelden.html"
URL_STRIESEN = "https://www.schachbund.de/verein/F2810.html"


class SpeichereDWZDaten:
    def setup_method(self, method):
        options = webdriver.FirefoxOptions()
        options.headless = True  # Headless-Modus aktivieren
        self.driver = webdriver.Firefox(options=options)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def writeFile(self, data, format: str) -> str:
        from datetime import datetime

        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = f"{basename}_{timestamp}.{format}"
        with open(filename, "w") as json_file:
            json_file.write(data)
        LOGGER.info("Written to " + filename)
        return filename

    def test_logoutLogin(self):
        # print("running profile " + self.driver.options["profile"] )
        self.driver.get(URL_LOGIN)
        # self.driver.set_window_size(1933, 1045)
        self.driver.find_element(By.ID, "username").send_keys(os.getenv("DWZ_USERNAME"))
        self.driver.find_element(By.ID, "password").send_keys(os.getenv("DWZ_PASSWORD"))
        self.driver.find_element(By.CSS_SELECTOR, ".submit").click()
        # Get all available cookies
        # print(self.driver.get_cookies())
        self.driver.get(URL_STRIESEN)
        dewisTable = self.driver.find_element(By.ID, "dewisTable")

        # Kopfzeile (Header) extrahieren
        headers = [
            header.text for header in dewisTable.find_elements(By.XPATH, PAT_HEADERS)
        ]
        # Datenzeilen extrahieren
        rows = dewisTable.find_elements(By.XPATH, PAT_ROWS)
        data = []
        for row in rows:
            cells = row.find_elements(By.XPATH, PAT_CELLS)
            data.append([cell.text for cell in cells])

        # DataFrame in JSON umwandeln
        df = pd.DataFrame(data, columns=headers)
        json_data = df.to_json(orient="records", indent=2)

        # JSON-Daten speichern
        return self.writeFile(json_data, format="json")

    # LOGGER.warning(msg=self.driver.save_screenshot( str(Path(__file__).parent / "Screenshots/login.png")))


def get_files_with_prefix(directory, prefix: str):
    matching_files = []

    for filename in os.listdir(directory):
        fn = filename.lower()
        if fn.startswith(prefix) and fn.endswith(".json"):
            matching_files.append(Path(directory) / filename)

    return matching_files


def compare_changes(file):
    # Return a new list containing all items from the iterable in ascending order.
    sorted_existing = sorted(get_files_with_prefix(".", basename))
    if len(sorted_existing) < 2:
        return
    LOGGER.debug(sorted_existing)
    newer = False
    with open(sorted_existing[-1], "r") as newest:
        with open(sorted_existing[-2], "r") as older:
            newer = newest.read() != older.read()

    LOGGER.log(
        logging.WARN if newer else logging.INFO, f"Found newer {basename}: {newer}!"
    )
    if newer and os.name == "nt":
        import ctypes

        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, "Differenz entdeckt", "Information SpeichereDWZDaten", 0)


# Dir with geckodriver
os.chdir(Path.home() / os.getenv("DWZ_PATH"))
LOGGER.info(f"Working in '{os.getcwd()}'")

suite = SpeichereDWZDaten()
suite.setup_method(None)
file_name = suite.test_logoutLogin()
suite.teardown_method(None)

compare_changes(file_name)
