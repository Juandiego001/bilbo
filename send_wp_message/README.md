# Send WhatsApp Message

Script desarrollado en Python para agilizar las pruebas de envío de mensajes mediante métodos POST hacia la API local de envío de mensajes de WhatsApp, especificando el puerto, el mensaje a enviar y el mensaje esperado en la respuesta.

## ¿Cómo utilizar el script?

Para utilizar el script primero se deben instalar las dependencias:

```bash
pip install -r requirements.txt
```

Posteriormente para utilizar el script basta con ejecutar:

```bash
python main.py
```

El script solicitará el puerto en el backend donde se está ejecutando la API. Normalmente es el puerto `5000`. Adicionalmente, solicitará el número de WhatsApp donde se desea recibir los mensajes.

Cuando se ejecuta por primera vez, estos valores ya quedan guardados para siempre aunque se pueden modificar directamente en el archivo `.env`.

El script entra en un ciclo donde ofrece 5 opciones:

```bash
1. Enviar un mensaje
2. Ver variables de entorno
3. Cambiar variables de entorno
4. Enviar un mensaje temporalmente a otro número
5. Finalizar
```

Finalmente se agregó que desde el backend se retorne la respuesta de la IA para poder ver en este script que mensaje estamos recibiendo a nuestro WhatsApp.
