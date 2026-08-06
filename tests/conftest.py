import os
import random
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://127.0.0.1:5000"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshots")

NOMBRES = [
    "juan", "maria", "carlos", "ana", "luis", "carmen", "pedro", "laura",
    "diego", "sofia", "andres", "valeria", "roberto", "diana", "oscar",
]

APELLIDOS = [
    "perez", "garcia", "martinez", "rodriguez", "sanchez", "diaz", "flores",
    "reyes", "castillo", "vargas", "torres", "ramirez", "gomez", "ruiz",
]


def correo_unico(dominio="@gmail.com"):
    return f"{random.choice(NOMBRES)}.{random.choice(APELLIDOS)}{random.randint(10, 99)}{dominio}"


def _driver_options():
    options = Options()
    if os.environ.get("HEADLESS"):
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    return options


@pytest.fixture()
def driver():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=_driver_options())
    drv.implicitly_wait(5)
    drv.set_window_size(1280, 800)
    yield drv
    drv.quit()


def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


def wait_for_text(driver, text, timeout=10):
    def _predicate(d):
        try:
            return text in d.find_element(By.TAG_NAME, "body").text
        except (StaleElementReferenceException, NoSuchElementException, WebDriverException):
            return False

    WebDriverWait(driver, timeout).until(_predicate)


def login(driver, username=ADMIN_USERNAME, password=ADMIN_PASSWORD):
    driver.get(f"{BASE_URL}/login")
    user = wait_for_element(driver, By.ID, "username")
    user.clear()
    user.send_keys(username)
    pwd = driver.find_element(By.ID, "password")
    pwd.clear()
    pwd.send_keys(password)
    click_submit(driver)


def click_submit(driver):
    driver.find_element(By.CSS_SELECTOR, "#content form button[type=submit]").click()


def wait_login_success(driver, timeout=10):
    WebDriverWait(driver, timeout).until(lambda d: d.current_url.rstrip("/") == BASE_URL)


@pytest.fixture()
def logged_in(driver):
    login(driver)
    wait_login_success(driver)
    return driver


def submit_force(driver):
    driver.execute_script(
        "var f=document.querySelector('#content form');"
        "f.querySelectorAll('[required]').forEach(function(e){e.removeAttribute('required')});"
        "f.submit();"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        driver = item.funcargs.get("driver")
        if driver is not None:
            try:
                os.makedirs(SCREENSHOT_DIR, exist_ok=True)
                path = os.path.join(SCREENSHOT_DIR, f"{item.name}_{report.outcome}.png")
                driver.save_screenshot(path)
            except Exception:
                pass
