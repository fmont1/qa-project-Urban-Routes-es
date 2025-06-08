# Proyecto QA - Urban Routes (Sprint 8)

Este proyecto automatiza el proceso completo de pedir un taxi en la aplicación web Urban Routes, utilizando **Selenium** y el **Patrón Page Object Model (POM)** como parte del Sprint 8 del bootcamp de QA Engineering.

---

## Funcionalidades Automatizadas

Las pruebas cubren las siguientes acciones en el flujo de pedido de taxi:

1. Ingresar la dirección de origen y destino.
2. Seleccionar la tarifa **Comfort**.
3. Ingresar el número de teléfono.
4. Agregar una tarjeta de crédito (con cambio de enfoque antes de hacer clic en "Enlazar").
5. Dejar un mensaje para el conductor.
6. Pedir una manta y pañuelos.
7. Pedir 2 helados.
8. Esperar a que aparezca el **modal de búsqueda de taxi**.
9. *(Opcional)* Esperar a que se muestre la información del conductor.

---

## Tecnologías Utilizadas

- Python 3.13
- Selenium 4.16.0
- Pytest
- WebDriver para Chrome

---

## Estructura del Proyecto

- `main.py`: contiene la clase `UrbanRoutesPage` y la clase de pruebas `TestUrbanRoutes`.
- `data.py`: contiene las variables necesarias para ejecutar las pruebas (direcciones, teléfono, tarjeta, mensaje, etc.).

---

## Notas Importantes: Consideraciones sobre la versión de Selenium

Durante el desarrollo de este proyecto se presentaron incompatibilidades entre el código proporcionado por el curso y las versiones más recientes de Selenium. En particular:
- El uso de desired_capabilities en setup_class() ya no es válido en Selenium 4. Sin embargo, se ha mantenido para conservar el código original del curso, aunque puede generar errores en ejecución.
- En el import statement, parte del código como from selenium.webdriver import Keys o el uso de expected_conditions sin alias (as EC) también presentan problemas si se usa Selenium moderno.
- Probablemente para permitir la correcta ejecución del código, podría ser necesario instalar una versión anterior de Selenium


---

## Cómo ejecutar las pruebas

1. Activa tu entorno virtual si aún no lo has hecho:
   ```bash
   .venv\Scripts\activate
   ```

2. Asegúrate de tener Selenium instalado:
   ```bash
   pip install selenium
   ```

3. Ejecuta las pruebas con `pytest`:
   ```bash
   pytest main.py
   ```

---

## Notas finales: Errores persisten a pesar de los cambios 

- He realizado todos los ajustes sugeridos por el revisor, desde compatibilidad hasta mejora de selectores, usando Keys.ENTER, ajustes en setup_class, WebDriverWait, etc., con la ayuda de Chat GPT; sin embargo, siguen fallando 8 pruebas, aparentemente por tiempos de carga o comportamiento inconsistente de la aplicación. Si es posible, agradecería una revisión orientada a entender qué está impidiendo que estas pruebas se ejecuten correctamente, ya que no hay errores de sintaxis ni uso incorrecto de Selenium y yo ya no sé qué más hacer ni puedo seguir invirtiendo más tiempo en esto hasta no saber qué está sucediendo.
---

¡Gracias por revisar este proyecto!
