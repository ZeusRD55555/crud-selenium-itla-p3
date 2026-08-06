import time
import pytest
from selenium.webdriver.common.by import By
from conftest import BASE_URL, logged_in, submit_force, wait_for_text, wait_for_element, click_submit


def unique_suffix():
    return int(time.time() * 1000)


@pytest.mark.usefixtures("logged_in")
class TestEditarUsuario:

    def _crear(self, driver, nombre, correo, telefono):
        driver.get(f"{BASE_URL}/usuarios/crear")
        wait_for_element(driver, By.ID, "nombre")
        driver.find_element(By.ID, "nombre").send_keys(nombre)
        driver.find_element(By.ID, "correo").send_keys(correo)
        driver.find_element(By.ID, "telefono").send_keys(telefono)
        click_submit(driver)
        wait_for_text(driver, "Usuario creado exitosamente.")

    def _buscar_editar(self, driver, nombre):
        driver.get(f"{BASE_URL}/usuarios?q={nombre}")
        link = wait_for_element(
            driver,
            By.XPATH,
            "//td[contains(text(), '" + nombre + "')]/..//a[contains(@href, '/usuarios/editar/')]",
        )
        link.click()

    def test_editar_usuario_correcto(self, driver):
        suf = unique_suffix()
        correo = f"editar{suf}@gmail.com"
        nombre_original = f"Nombre Original {suf}"
        nombre_editado = f"Nombre Editado {suf}"
        self._crear(driver, nombre_original, correo, "809-555-1234")
        self._buscar_editar(driver, nombre_original)
        wait_for_element(driver, By.ID, "nombre")
        nombre = driver.find_element(By.ID, "nombre")
        nombre.clear()
        nombre.send_keys(nombre_editado)
        click_submit(driver)
        wait_for_text(driver, "Usuario actualizado exitosamente.")
        driver.get(f"{BASE_URL}/usuarios?q={nombre_editado}")
        wait_for_text(driver, nombre_editado)

    def test_editar_usuario_correo_duplicado(self, driver):
        suf = unique_suffix()
        correo_a = f"dupla{suf}@itla.edu.do"
        correo_b = f"duplb{suf}@gmail.com"
        nombre_a = f"Usuario A {suf}"
        nombre_b = f"Usuario B {suf}"
        self._crear(driver, nombre_a, correo_a, "809-555-1000")
        self._crear(driver, nombre_b, correo_b, "809-555-2000")
        self._buscar_editar(driver, nombre_b)
        wait_for_element(driver, By.ID, "correo")
        correo_field = driver.find_element(By.ID, "correo")
        correo_field.clear()
        correo_field.send_keys(correo_a)
        click_submit(driver)
        wait_for_text(driver, "El correo ya está registrado por otro usuario.")

    def test_editar_usuario_nombre_vacio(self, driver):
        suf = unique_suffix()
        correo = f"limite{suf}@itla.edu.do"
        nombre = f"Usuario Limite {suf}"
        self._crear(driver, nombre, correo, "809-555-3000")
        self._buscar_editar(driver, nombre)
        wait_for_element(driver, By.ID, "nombre")
        field = driver.find_element(By.ID, "nombre")
        field.clear()
        submit_force(driver)
        wait_for_text(driver, "El nombre es obligatorio.")
