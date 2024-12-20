# AppBasesdatos

Rest API utilizando Django Rest Framework para la aplicación.

# Instalación

Clonamos el repositorio

```bash
git clone https://github.com/anderson-usme/trabajos.git
cd trabajos
```

Se crea el env virtual.

```bash
pip install virtualenv
python3 -m venv venv

```
Activamos el env virtual e instalamos dependencias

```bash
source venv/bin/activate
pip install -r requirements.txt
```
Ejecutamos el proyecto:

```python
python manage.py runserver
```
## Uso de las rutas

```
Register

```
```
 se llama a la ruta http://127.0.0.1:8000/api/register/ y se ingresa el objeto de esta forma con esta ruta creamos el usuario con el cual podremos conseguir el token y el refresh un ejemplo de como se deberia ver el objeto es :

 {

    "username": 
      "daniel1"
    ,
    "password": 
      "patito123"

}

```
Delete
```
se llama a la ruta http://localhost:8000/api/eliminar_servidor/nombre_del_servidor/ y se ingresa el nombre del servidor que deseamos borrar esta ruta cuenta con autenticacion se tiene que pasar una peticion delete

```
pausar servidor
```
se llama la ruta http://localhost:8000/api/pausar_servidor/nombre_del_servidor/ y se ingresa el nombre del servidor que deseamos pausar esta ruta requiere autenticacion se tiene que pasar una peticion post
```
Reanudar servidor
```
se llama la ruta http://localhost:8000/api/reanudar_servidor/nombre_del_servidor/ y se ingresa el nombre del servidor que deseamos reanudar esta ruta requiere autenticacion se tiene que pasar una peticion post
```
Token

```

se llama a la ruta http://127.0.0.1:8000/api/token/ para conseguir un token y un refresh que se tendran que dar en el ingresar servidor para poder agregar uno el objeto a ingresar en esta ruta es exactamente el mismo que en el register

```
Agregar servidor

```
se llama a la ruta  http://localhost:8000/api/agregar_servidor/ pero para poder aceder a ella en los HTTP Headers tienes que activar un header que sea Authorization seguido del token que tiene que ir acompañado de un Bearer mas el token que nos tendrian que haber dado en la ruta anterior el objeto se deberia ver de la siguiente forma:


{
    "name": "prueba1",
    "location": "aqui al lado",
    "services": [
        {
            "backend": {
                "url": "http://127.0.0.1:3000/",
                "status": "" 
            },
            "frontend": {
                "url": "http://127.0.0.1:3000/",
                "status": ""  
            }
        }
    ]
}
```
Check url

```

se llama a la ruta http://127.0.0.1:8000/api/check_url/ y esta nos da un status general y el estado de cada uno de los servidores ingresados

```
### Dockerizacion

```
El puerto de salida se define en el archivo `docker-compose.yml`:

```
ports:
  - 8000:8000
```
