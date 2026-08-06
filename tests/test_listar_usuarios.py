import time
import pytest
from selenium.webdriver.common.by import By
from conftest import BASE_URL, logged_in, wait_for_text, wait_for_element, click_submit


@pytest.mark.usefixtures("logged_in")
class TestListarUsuarios:

    def test_listar_usuario_creado(self, driver):
        nombre = f"Listado Usuario {int(time.time())}"
        correo = f"listado{int(time.time() * 1000)}@itla.edu.do"
        driver.get(f"{BASE_URL}/usuarios/crear")
        wait_for_element(driver, By.ID, "nombre")
        driver.find_element(By.ID, "nombre").send_keys(nombre)
        driver.find_element(By.ID, "correo").send_keys(correo)
        driver.find_element(By.ID, "telefono").send_keys("809-555-0001")
        click_submit(driver)
        wait_for_text(driver, "Usuario creado exitosamente.")
        driver.get(f"{BASE_URL}/usuarios")
        wait_for_text(driver, nombre)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert correo in body

    def test_listar_sin_resultados(self, driver):
        driver.get(f"{BASE_URL}/usuarios?q=inexistente_zz")
        wait_for_text(driver, "No hay usuarios registrados.")

    def test_listar_busqueda_extremadamente_larga(self, driver):
        driver.get(f"{BASE_URL}/usuarios?q={'a' * 255}")
        wait_for_text(driver, "Usuarios")
