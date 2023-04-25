# Landbot Backend Challenge

## Arquitectura. El Framework

He elegido FastAPI para desarrollar el proyecto por los siguientes motivos

- El proyecto se plantea como un servicio anexo a otro proyecto por lo que se requiere un framework que se acople fácilmente como servicio externo.

- solo se plantea la creación de un API REST sin backoffice ni gestión de usuarios.

- Al tratarse de una aplicación de mensajería se requiere que reciba rápidamente muchas peticiones y sea escalable horizontalmente.

- Se puede integrar con cualquier bbdd y/o ORM, en este caso se ha usado sqlite para la gestión de la información dinámica del proyecto con Tortoise ORM que es más facil de implementar que SQL Alchemy y mantiene la arquitectura asíncrona del proyecto, pero se podría integrar con otras fuentes de datos.

## Arquitectura. El patrón Plugin

Para la implementación de la solución se ha elegido el patrón de diseño Plugin que permite cargar dinámicamente clases, cada una con su funcionalidad específica buscando en este cas en un directorio.

Para la búsqueda, se ha contemplado que en el directorio de plugins, cada plugin puede estar en un directorio con el nombre que sea y dentro de deste, en un archivo .py también de nombre arbitrario hay que crear una clase que implemente el interface propuesto, que de momento solo pide implementar el método

send_message(self, message, background_tasks: BackgroundTasks)

que como se puede ver tiene como parámetros el mensaje creado con una clase de Pydantic y el objeto que usa FastAPI para la ejecución de tareas en segundo plano.

Con esta solución, se podría escribir un plugin para cualquier tipo de mensajería con su funcionalidad propia con tan solo crear un nuevo directorio, un archivo y extender el interfaz.

## Ejecución de tareas

Puesto que la ejecución de las tareas se hacen en segundo plano y por la arquitectura asíncrona de FastAPI para empezar puede ser una solución razonable y escalable horizontalmente haciendo réplicas de los nodos de FastAPI, pero si llegado el momento se considera que esta forma se convierte en un cuello de botella se podría implementar una integración con un sistema de colas como Celery con RabbitMQ de forma que cada mensaje se derive a una cola y que sean los workers de Celery los que ejecuten las tareas y escalen dejando el FastAPI solo para la recepción de los mensajes.

## Modelo de datos

Para el proyecto se ha contemplado la creación de varias entidades de datos, algunas persistentes en la bbdd

### Mensaje

Estrunctura para difinir el mensaje de entrada que como se plantea tiene los campos

topic y channel, ambos de tipo string

no se guardan en bbdd, pero sería una buena opción guardar un log con todas las entradas y con el resultado del envio del mensaje en un log para poder hacer un seguimiento de lo ocurrido.

### Topic

Esta entidad se guarda en bbdd y nos permite obtener el canal al que se lanzará el mensaje dado un Topic en el mensaje de entrada. Tiene como campos name y channel que es una relación con la entidad Channel que se detalla a continuación.

### Channel

En esta entidad definimos la clase que hay que buscar en el directorio de plugins para poder cargarla dinámicamente y hacer uso de ella. Si no estuviera bien configurada esta tabla los plugins no hacen su trabajo.

Se ha habilitado endpoints para crear nuevos Topics y Channels lo cual se podría hacer desde un interfaz en el proyecto pricipal llamando a estos enpoints.

### Autenticación

En este caso no se ha implementado ningún tipo de implementación, si bien, aunque los endpoints podrían ponerse en una red interna sin acceso al exterior y solo expuestos a llamadas del proyecto principal y por lo tanto no necesitar una autenticación, se poedrían securizar facilmente con el empleo de jwt tokens creados por un tercer sistema lo cual mantendría el servicio seguro y rápido.

### Email implementation

Se ha implementado el envio de un email en un plugin llamado email en el directorio de plugins y se le ha adjuntado un archivo .env con las varibles de entorno de forma que cuando se pase a producción esas varibles se guardan como secretos en el sistema de despliegue y el plugin funciona con la configuración correspondiente a su entorno (dev, staging, pro...)
