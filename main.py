import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


# no modificar
def retrieve_phone_code(driver) -> str:
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
    return None


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_taxi_button = (By.CLASS_NAME, 'button.round')
    comfort_tariff_button = (By.XPATH, "//div[contains(@class, 'tcard') and .//div[@class='tcard-title' and text()='Comfort']]")
    phone_field = (By.ID, 'phone')
    next_button = (By.CLASS_NAME, 'button.full')
    phone_code_field = (By.ID, 'code')
    confirm_button = (By.XPATH, "//button[contains(@class, 'button') and text()='Confirmar']")
    payment_method_button = (By.CLASS_NAME, 'pp-text')
    add_card_button = (By.CLASS_NAME, 'pp-row.disabled')
    card_number_field = (By.ID, 'number')
    card_cvv_field = (By.XPATH, "//input[@id='code' and @class='card-input']")
    link_card_button = (By.XPATH, "//button[contains(@class, 'button') and text()='Enlazar']")
    close_payment_modal = (By.XPATH, "//div[@class='payment-picker close-button']")
    message_field = (By.ID, 'comment')
    blanket_checkbox = (By.CLASS_NAME, 'slider.round')
    blanket_switch = (By.XPATH, "//div[@class='r-sw']//div[@class='switch']")
    ice_cream_counter_plus = (By.XPATH, "//div[@class='counter-plus']")
    ice_cream_value = (By.XPATH, "//div[@class='counter-value']")
    order_taxi_button = (By.CLASS_NAME, 'smart-button')
    modal_searching_taxi = (By.CLASS_NAME, 'order-body')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.from_field))
        from_element = self.driver.find_element(*self.from_field)
        from_element.clear()
        from_element.send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.to_field))
        to_element = self.driver.find_element(*self.to_field)
        to_element.clear()
        to_element.send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_call_taxi(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.call_taxi_button))
        self.driver.find_element(*self.call_taxi_button).click()

    def select_comfort_tariff(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.comfort_tariff_button))
        self.driver.find_element(*self.comfort_tariff_button).click()

    def get_comfort_tariff_class(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.comfort_tariff_button))
        return self.driver.find_element(*self.comfort_tariff_button).get_attribute("class")

    def click_phone_field(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.phone_field))
        self.driver.find_element(*self.phone_field).click()

    def enter_phone_number(self, phone):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.phone_field))
        phone_element = self.driver.find_element(*self.phone_field)
        phone_element.clear()
        phone_element.send_keys(phone)

    def click_next_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.next_button))
        self.driver.find_element(*self.next_button).click()

    def enter_phone_code(self, code):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.code_field))
        self.driver.find_element(*self.code_field).send_keys(code)

    def click_confirm_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.confirm_button))
        self.driver.find_element(*self.confirm_button).click()

    def click_payment_method(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.payment_method_button))
        self.driver.find_element(*self.payment_method_button).click()

    def click_add_card(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.add_card_button))
        self.driver.find_element(*self.add_card_button).click()

    def enter_card_number(self, card_number):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.card_number_field))
        self.driver.find_element(*self.card_number_field).send_keys(card_number)

    def enter_card_cvv(self, cvv):
        # Esperar más tiempo y usar un localizador más específico
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.card_cvv_field))
        cvv_element = self.driver.find_element(*self.card_cvv_field)
        cvv_element.clear()
        cvv_element.send_keys(cvv)
        # Cambiar el foco para activar el botón "Enlazar"
        cvv_element.send_keys(Keys.TAB)

    def click_link_card(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.link_card_button))
        self.driver.find_element(*self.link_card_button).click()

    def close_payment_modal_window(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.close_payment_modal))
        self.driver.find_element(*self.close_payment_modal).click()

    def enter_message_for_driver(self, message):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.message_field))
        message_element = self.driver.find_element(*self.message_field)
        message_element.clear()
        message_element.send_keys(message)

    def get_message_for_driver(self):
        return self.driver.find_element(*self.message_field).get_property('value')

    def click_blanket_switch(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.blanket_switch))
        self.driver.find_element(*self.blanket_switch).click()

    def get_blanket_status(self):
        blanket_element = self.driver.find_element(*self.blanket_switch)
        return blanket_element.find_element(By.XPATH, "//input[@class='switch-input']").is_selected()

    def click_ice_cream_plus(self, times=1):
        for _ in range(times):
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ice_cream_counter_plus))
            self.driver.find_element(*self.ice_cream_counter_plus).click()

    def get_ice_cream_quantity(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.ice_cream_value))
        return self.driver.find_element(*self.ice_cream_value).text

    def click_order_taxi(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.order_taxi_button))
        self.driver.find_element(*self.order_taxi_button).click()

    def wait_for_search_modal(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.modal_searching_taxi))

    def is_search_modal_visible(self):
        try:
            element = self.driver.find_element(*self.modal_searching_taxi)
            return element.is_displayed()
        except:
            return False

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import ChromeOptions
        options = ChromeOptions()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)

    def setup_method(self):
        self.driver.get(data.urban_routes_url)

    # Prueba 1: Configurar la dirección
    def test_set_route(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)

        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    # Prueba 2: Seleccionar la tarifa "Comfort"
    def test_select_comfort_tariff(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_call_taxi()
        routes_page.select_comfort_tariff()

        assert "active" in routes_page.get_comfort_tariff_class()

    # Prueba 3: Rellenar el número de teléfono
    def test_fill_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_call_taxi()
        routes_page.select_comfort_tariff()  # Agregar este paso
        time.sleep(2)  # Esperar a que aparezca el campo de teléfono
        routes_page.click_phone_field()
        routes_page.enter_phone_number(data.phone_number)
        routes_page.click_next_button()

        # Obtener el código de confirmación
        code = retrieve_phone_code(self.driver)
        routes_page.enter_phone_code(code)
        routes_page.click_confirm_button()

        # Verificar que el teléfono se guardó correctamente
        phone_element = self.driver.find_element(*routes_page.phone_field)
        assert data.phone_number in phone_element.get_property('value')

    # Prueba 4: Agregar una tarjeta de crédito
    def test_add_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_call_taxi()
        routes_page.select_comfort_tariff()  # Agregar este paso
        time.sleep(2)  # Esperar a que la interfaz se cargue
        routes_page.click_payment_method()
        time.sleep(1)  # Esperar a que se abra el modal
        routes_page.click_add_card()
        time.sleep(1)  # Esperar a que se abra el modal de agregar tarjeta
        routes_page.enter_card_number(data.card_number)
        routes_page.enter_card_cvv(data.card_code)
        routes_page.click_link_card()
        routes_page.close_payment_modal_window()

        # Verificar que se agregó la tarjeta (el método de pago cambió)
        payment_element = self.driver.find_element(*routes_page.payment_method_button)
        assert "Tarjeta" in payment_element.text

    # Prueba 5: Escribir un mensaje para el conductor
    def test_write_message_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_call_taxi()
        routes_page.enter_message_for_driver(data.message_for_driver)

        assert routes_page.get_message_for_driver() == data.message_for_driver

    # Prueba 6: Pedir una manta y pañuelos
    def test_request_blanket_and_tissues(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_call_taxi()
        routes_page.click_blanket_switch()

        assert routes_page.get_blanket_status() == True

    # Prueba 7: Pedir 2 helados
    def test_order_ice_cream(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_call_taxi()
        routes_page.click_ice_cream_plus(2)

        assert routes_page.get_ice_cream_quantity() == "2"

    # Prueba 8: Aparece el modal para buscar un taxi
    def test_search_taxi_modal_appears(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_call_taxi()
        routes_page.click_order_taxi()
        routes_page.wait_for_search_modal()

        assert routes_page.is_search_modal_visible() == True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
