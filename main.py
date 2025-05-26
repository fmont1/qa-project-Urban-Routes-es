import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    comfort_tariff_button = (By.CLASS_NAME, 'tariff-card_comfort')
    phone_field = (By.ID, 'phone')
    add_card_button = (By.CLASS_NAME, 'payment-method__add-button')
    card_number_field = (By.ID, 'number')
    card_expiration_date_field = (By.ID, 'exp')
    card_cvv_field = (By.ID, 'code')
    link_card_button = (By.CLASS_NAME, 'modal__button')
    message_field = (By.ID, 'comment')
    blanket_checkbox = (By.ID, 'blanket')
    tissues_checkbox = (By.ID, 'towels')
    ice_cream_field = (By.ID, 'ice-cream')
    modal_searching_taxi = (By.CLASS_NAME, 'search-form__modal')
    driver_info = (By.CLASS_NAME, 'order-card')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff_button).click()

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def enter_phone_number(self, phone):
        self.driver.find_element(*self.phone_field).send_keys(phone)

    def add_card(self, number, expiry, cvv):
        self.driver.find_element(*self.add_card_button).click()
        self.driver.find_element(*self.card_number_field).send_keys(number)
        self.driver.find_element(*self.card_expiration_date_field).send_keys(expiry)
        cvv_input = self.driver.find_element(*self.card_cvv_field)
        cvv_input.send_keys(cvv)

        # Cambio de enfoque
        self.driver.find_element(*self.card_number_field).click()
        self.driver.find_element(*self.link_card_button).click()

    def leave_message_for_driver(self, message):
        self.driver.find_element(*self.message_field).send_keys(message)

    def request_blanket_and_tissues(self):
        self.driver.find_element(*self.blanket_checkbox).click()
        self.driver.find_element(*self.tissues_checkbox).click()

    def order_ice_cream(self, quantity):
        self.driver.find_element(*self.ice_cream_field).send_keys(str(quantity))

    def wait_for_search_modal(self):
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.modal_searching_taxi)
        )

    def wait_for_driver_info(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.driver_info)
        )

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_add_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # 1. Ingresar direcciones
        routes_page.set_route(data.address_from, data.address_to)

        # 2. Seleccionar tarifa Comfort
        routes_page.select_comfort_tariff()

        # 3. Ingresar teléfono
        routes_page.enter_phone_number(data.phone_number)

        # 4. Agregar tdc
        routes_page.add_card(data.card_number, '12/25', data.card_code)

        # 5. Dejar mensaje para el conductor
        routes_page.leave_message_for_driver(data.message_for_driver)

        # 6. Pedir manta y pañuelos
        routes_page.request_blanket_and_tissues()

        # 7. Pedir 2 helados
        routes_page.order_ice_cream(2)

        # 8. Esperar modal de búsqueda de taxi
        routes_page.wait_for_search_modal()

        # 9. Esperar info del conductor (opcional)
        routes_page.wait_for_driver_info()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
