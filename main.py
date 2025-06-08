import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

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
    comfort_tariff_button = (By.CLASS_NAME, 'tariff-card_comfort')
    call_taxi_button = (By.CLASS_NAME, 'confirm-button')
    phone_field = (By.ID, 'phone')
    add_card_button = (By.CLASS_NAME, 'payment-method__add-button')
    card_number_field = (By.ID, 'number')
    card_cvv_field = (By.ID, 'code')
    link_card_button = (By.CLASS_NAME, 'modal__button')
    message_field = (By.ID, 'comment')
    blanket_button = (By.ID, 'blanket-and-towels')
    ice_cream_field = (By.ID, 'ice-cream')
    modal_searching_taxi = (By.CLASS_NAME, 'search-form__modal')
    driver_info = (By.CLASS_NAME, 'order-card')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        field = self.driver.find_element(*self.from_field)
        field.send_keys(from_address)
        field.send_keys(Keys.ENTER)

    def set_to(self, to_address):
        field = self.driver.find_element(*self.to_field)
        field.send_keys(to_address)
        field.send_keys(Keys.ENTER)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff_button).click()

    def click_call_taxi(self):
        self.driver.find_element(*self.call_taxi_button).click()

    def enter_phone_number(self, phone):
        element = self.driver.find_element(*self.phone_field)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.send_keys(phone)

    def add_card(self, number, cvv):
        self.driver.find_element(*self.add_card_button).click()
        self.driver.find_element(*self.card_number_field).send_keys(number)
        self.driver.find_element(*self.card_cvv_field).send_keys(cvv)
        self.driver.find_element(*self.card_number_field).click()
        self.driver.find_element(*self.link_card_button).click()

    def leave_message_for_driver(self, message):
        self.driver.find_element(*self.message_field).send_keys(message)

    def request_blanket_and_towels(self):
        self.driver.find_element(*self.blanket_button).click()

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
        from selenium.webdriver import ChromeOptions
        options = ChromeOptions()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)

    def test_set_from(self):
        self.driver.get(data.urban_routes_url)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'from'))
        )
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        routes_page.set_from(address_from)
        assert routes_page.get_from() == address_from

    def test_set_to(self):
        routes_page = UrbanRoutesPage(self.driver)
        address_to = data.address_to
        routes_page.set_to(address_to)
        assert routes_page.get_to() == address_to

    def test_select_comfort_tariff(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(UrbanRoutesPage.comfort_tariff_button)
        )
        routes_page.select_comfort_tariff()
        assert True

    def test_click_call_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(UrbanRoutesPage.call_taxi_button)
        )
        routes_page.click_call_taxi()
        assert True

    def test_enter_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(UrbanRoutesPage.phone_field)
        )
        routes_page.enter_phone_number(data.phone_number)
        assert True

    def test_add_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(UrbanRoutesPage.add_card_button)
        )
        routes_page.add_card(data.card_number, data.card_code)
        assert True

    def test_leave_message_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(UrbanRoutesPage.message_field)
        )
        routes_page.leave_message_for_driver(data.message_for_driver)
        assert True

    def test_request_blanket_and_towels(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(UrbanRoutesPage.blanket_button)
        )
        routes_page.request_blanket_and_towels()
        assert True

    def test_order_ice_cream(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(UrbanRoutesPage.ice_cream_field)
        )
        routes_page.order_ice_cream(2)
        assert True

    def test_wait_for_search_modal(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_search_modal()
        assert True

    def test_wait_for_driver_info(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_driver_info()
        assert True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
