# AppBasesdatos

Rest API utilizando Django Rest Framework para la aplicación TerraInfo.

# Instalación

Clonamos el repositorio

```
git clone https://github.com/anderson-usme/trabajos.git
cd trabajos
```

Se crea el env virtual.

## Clonamos el repositorio

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
## dockerizacion

```
El puerto de salida se define en el archivo `docker-compose.yml`:

```
ports:
  - 8000:8000
```
