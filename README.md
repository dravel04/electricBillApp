# Light Calculator
App en python que dados los valores de una factura de electrica, los compare con los datos cargados de tarifas de proveedores y nos diga cual es la tarifa que más nos interesa.

## UI
Lo primero que haremos es la UI. Tendrá 2 opciones:
1. **Nuevo Perfil:** Nos pedirá los datos su tarifa actual:
    - Identificador del perfil
    - Datos de potencia:
        - Punta / Valle
    - Datos de energia:
        - Punta / Llano / Valle
    - ¿Solar?
        - Excedentes (KW)
        - Precio al que se los pagan

2. **Perfiles (solo saldrá en caso de que existe algun prefil ya creado):** Listado de los perfiles registrados. Este listado será numerico: *1,2,3...* Dentro de cada perfil tendremos la siguientes opciones
    - **Editar perfil:** Una vez entramos en esta opción, se nos mostrarán los datos del perfil actual -> visualizar el diccionario completo. Se nos dará la opción de editar cualquiera de los campos mediante un número. Cada campo corresponderá a un numero comenzando por el 1. Cada vez que cambiemos un campos actualizaremos el diccionario cargado en memoria. La última opción numerica será guardar los cambios, esto pasará los cambios al fichero `profiles.json`
    - **Lanzar comparativa:** Tiene la lógica completa de la comparación. Cruza los datos introducidos por el usuario en el perfil, con los datos de las tarifas guardadas.

### Logica
Al crear un nuevo perfil, este generará un diccionario con los campos marcados y se guardará como fichero en la ruta del script. Se genará un fichero por perfil.

