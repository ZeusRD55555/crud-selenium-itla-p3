import time
import pytest
from selenium.webdriver.common.by import By
from conftest import BASE_URL, logged_in, wait_for_text, wait_for_element, click_submit


def unique_suffix():
    return int(time.time() * 1000)


@pytest.mark.usefixtures("logged_in")
class TestEliminarUsuario:

    def _crear(self, driver, nombre, correo, telefono):
        driver.get(f"{BASE_URL}/usuarios/crear")
        wait_for_element(driver, By.ID, "nombre")
        driver.find_element(By.ID, "nombre").send_keys(nombre)
        driver.find_element(By.ID, "correo").send_keys(correo)
        driver.find_element(By.ID, "telefono").send_keys(telefono)
        click_submit(driver)
        wait_for_text(driver, "Usuario creado exitosamente.")

    def _clic_eliminar(self, driver, nombre, confirmar=True):
        driver.get(f"{BASE_URL}/usuarios?q={nombre}")
        boton = wait_for_element(
            driver,
            By.XPATH,
            "//td[contains(text(), '" + nombre + "')]/..//button[contains(text(), 'Eliminar')]",
        )
        if confirmar:
            driver.execute_script("window.confirm = function(){ return true; };")
        else:
            driver.execute_script("window.confirm = function(){ return false; };")
        boton.click()

    def test_eliminar_usuario_correcto(self, driver):
        suf = unique_suffix()
        nombre = f"Usuario a Borrar {suf}"
        correo = f"borrar{suf}@gmail.com"
        self._crear(driver, nombre, correo, "809-555-7777")
        self._clic_eliminar(driver, nombre)
        wait_for_text(driver, "Usuario eliminado exitosamente.")
        driver.get(f"{BASE_URL}/usuarios?q={nombre}")
        wait_for_text(driver, "No hay usuarios registrados.")

    def test_eliminar_usuario_inexistente(self, driver):
        status = driver.execute_script(
            "return fetch('/usuarios/eliminar/999999', {method: 'POST'}).then(function(r){ return r.status; });"
        )
        assert status == 404

    def test_eliminar_usuario_cancelado(self, driver):
        suf = unique_suffix()
        nombre = f"Usuario Cancelado {suf}"
        correo = f"cancelar{suf}@itla.edu.do"
        self._crear(driver, nombre, correo, "809-555-8888")
        self._clic_eliminar(driver, nombre, confirmar=False)
        driver.get(f"{BASE_URL}/usuarios?q={nombre}")
        wait_for_text(driver, nombre)
