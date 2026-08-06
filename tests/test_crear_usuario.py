import pytest
from selenium.webdriver.common.by import By
from conftest import BASE_URL, logged_in, wait_for_text, wait_for_element, submit_force, click_submit, correo_unico


@pytest.mark.usefixtures("logged_in")
class TestCrearUsuario:

    def _crear(self, driver, nombre, correo, telefono):
        driver.get(f"{BASE_URL}/usuarios/crear")
        wait_for_element(driver, By.ID, "nombre")
        driver.find_element(By.ID, "nombre").send_keys(nombre)
        driver.find_element(By.ID, "correo").send_keys(correo)
        driver.find_element(By.ID, "telefono").send_keys(telefono)
        click_submit(driver)

    def test_crear_usuario_correcto(self, driver):
        correo = correo_unico()
        self._crear(driver, "Nuevo Usuario", correo, "809-555-1111")
        wait_for_text(driver, "Usuario creado exitosamente.")
        driver.get(f"{BASE_URL}/usuarios?q=Nuevo Usuario")
        wait_for_text(driver, "Nuevo Usuario")
        body = driver.find_element(By.TAG_NAME, "body").text
        assert correo in body

    def test_crear_usuario_correo_duplicado(self, driver):
        correo = correo_unico()
        self._crear(driver, "Primer Usuario", correo, "809-555-2222")
        wait_for_text(driver, "Usuario creado exitosamente.")
        self._crear(driver, "Segundo Usuario", correo, "809-555-3333")
        wait_for_text(driver, "El correo ya está registrado.")

    def test_crear_usuario_nombre_vacio(self, driver):
        correo = correo_unico()
        driver.get(f"{BASE_URL}/usuarios/crear")
        wait_for_element(driver, By.ID, "correo")
        driver.find_element(By.ID, "correo").send_keys(correo)
        driver.find_element(By.ID, "telefono").send_keys("809-555-4444")
        submit_force(driver)
        wait_for_text(driver, "El nombre es obligatorio.")
