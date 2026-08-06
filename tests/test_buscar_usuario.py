import time
import pytest
from selenium.webdriver.common.by import By
from conftest import BASE_URL, logged_in, wait_for_text, wait_for_element, click_submit


def unique_email(prefix="buscar"):
    return f"{prefix}{int(time.time() * 1000)}@gmail.com"


@pytest.mark.usefixtures("logged_in")
class TestBuscarUsuario:

    def _crear(self, driver, nombre, correo, telefono):
        driver.get(f"{BASE_URL}/usuarios/crear")
        wait_for_element(driver, By.ID, "nombre")
        driver.find_element(By.ID, "nombre").send_keys(nombre)
        driver.find_element(By.ID, "correo").send_keys(correo)
        driver.find_element(By.ID, "telefono").send_keys(telefono)
        click_submit(driver)
        wait_for_text(driver, "Usuario creado exitosamente.")

    def _buscar(self, driver, texto):
        driver.get(f"{BASE_URL}/usuarios")
        q = wait_for_element(driver, By.NAME, "q")
        q.clear()
        q.send_keys(texto)
        click_submit(driver)

    def test_buscar_usuario_encontrado(self, driver):
        nombre = f"Persona Busqueda {int(time.time())}"
        correo = unique_email()
        self._crear(driver, nombre, correo, "809-555-9000")
        self._buscar(driver, nombre)
        wait_for_text(driver, nombre)
        body = driver.find_element(By.TAG_NAME, "body").text
        assert correo in body

    def test_buscar_usuario_sin_resultados(self, driver):
        self._buscar(driver, "zzz_no_existe_999")
        wait_for_text(driver, "No hay usuarios registrados.")

    def test_busqueda_vacia_muestra_todos(self, driver):
        driver.get(f"{BASE_URL}/usuarios")
        wait_for_element(driver, By.NAME, "q")
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        driver.get(f"{BASE_URL}/usuarios?q=")
        q = wait_for_element(driver, By.NAME, "q")
        assert q.get_attribute("value") == ""
        rows_vacio = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        assert len(rows_vacio) >= len(rows)
