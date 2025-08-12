import glob, pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import urljoin

def get_unit_tests():
  l = []
  for filepath in glob.glob("unit/test_*.js"):
    l.append(pytest.param("src/" + filepath[5:-3] + ".htm", id=filepath[5:-3]))
  return l

def test_unit(subtests, selenium, base_url):
  wait = WebDriverWait(selenium, 30)
  for test in get_unit_tests():
    test_url, = test.values
    with subtests.test(test.id):
      selenium.get(urljoin(base_url, test_url))
      wait.until(EC.visibility_of_element_located((By.ID, "logBar")))
      wait.until(EC.title_contains("Test PASSED"));
