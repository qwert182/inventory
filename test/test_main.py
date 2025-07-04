from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from urllib.parse import urljoin

def test_main(subtests, selenium, base_url):
  selenium.get(urljoin(base_url, "src/"))
  wait = WebDriverWait(selenium, 30)
  wait.until(EC.url_matches("#dbConnect$"))
  with subtests.test("github_example_repo"):
    wait.until(EC.visibility_of_element_located((By.ID, "dbConnectURL")))
    selenium.find_element(By.ID, "dbConnectURL").send_keys(urljoin(base_url, "https://github.com/example/repo"))
    element = selenium.find_element(By.ID, "dbConnectToken")
    element.send_keys("test_token_0000")
    element.send_keys(Keys.RETURN)
    wait.until(EC.url_matches("#main$"))
