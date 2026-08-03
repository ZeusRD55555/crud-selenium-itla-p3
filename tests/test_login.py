import pytest
from selenium.webdriver.common.by import By
from conftest import BASE_URL, login, submit_force, wait_for_text, wait_for_element, wait_login_success


@pytest.mark.usefixtures("driver")
class TestLogin:

    def test_login_correcto(self, driver):
        login(driver)
        wait_login_success(driver)
        assert driver.current_url == f"{BASE_URL}/"
        body = driver.find_element(By.TAG_NAME, "body").text
        assert "Bienvenido, admin" in body

    def test_login_incorrecto(self, driver):
        login(driver, password="clave-incorrecta")
        wait_for_text(driver, "Usuario o contraseña incorrectos.")
        assert driver.current_url == f"{BASE_URL}/login"

    def test_login_campos_vacios(self, driver):
        driver.get(f"{BASE_URL}/login")
        wait_for_element(driver, By.ID, "username")
        submit_force(driver)
        wait_for_text(driver, "Usuario o contraseña incorrectos.")
        assert driver.current_url == f"{BASE_URL}/login"
