# Cloud Backup & Audit System (CBAS) - Guía de Despliegue

Esta guía detalla los pasos necesarios para inicializar, configurar y ejecutar el sistema CBAS en tu entorno local.

## Paso 1: Instalación de Dependencias

Asegúrate de tener Python instalado en tu sistema. Abre una terminal de comandos (PowerShell, CMD o Bash) en la carpeta principal del proyecto y ejecuta el siguiente comando para instalar las librerías necesarias (Flask, Watchdog, SDK de Dropbox):

```bash
pip install -r requirements.txt
```

## Paso 2: Configuración de Credenciales Base

Crea un archivo llamado exactamente `.env` en la raíz del proyecto. Este archivo almacenará tus variables de entorno de forma segura.

Debes obtener la **Clave** (App Key) y el **Secreto** (App Secret) desde la [App Console de Dropbox](https://www.dropbox.com/developers/apps). Agrega el siguiente contenido al archivo `.env` (reemplazando los valores):

```env
DROPBOX_APP_KEY=tu_clave_de_aplicacion
DROPBOX_APP_SECRET=tu_secreto_de_aplicacion
PORT=5050
```

## Paso 3: Generación del Refresh Token (Token Permanente)

Para asegurar que el sistema no se desconecte cada 4 horas, necesitamos generar un token de acceso permanente (Offline).

1. Ejecuta el script de autorización en tu terminal:
   ```bash
   python obtener_token.py
   ```
2. El script te mostrará un enlace. Ábrelo en tu navegador.
3. Inicia sesión en Dropbox y haz clic en **"Permitir"** para autorizar la aplicación.
4. Dropbox te proporcionará un **código de autorización**. Cópialo y pégalo en la terminal.
5. La terminal te devolverá un **Refresh Token** largo. Cópialo y agrégalo a tu archivo `.env` para que quede así:

```env
DROPBOX_APP_KEY=tu_clave_de_aplicacion
DROPBOX_APP_SECRET=tu_secreto_de_aplicacion
DROPBOX_REFRESH_TOKEN=tu_nuevo_refresh_token_generado
PORT=5050
```

## Paso 4: Inicialización del Entorno Local

Verifica que exista una carpeta llamada `directorio_pyme` en la raíz de tu proyecto. 
Si no existe, créala:
```bash
mkdir directorio_pyme
```
*Nota: Este es el directorio de trabajo que el agente (Watchdog) vigilará en tiempo real para respaldar los cambios.*

## Paso 5: Ejecución del Núcleo del Sistema

Una vez configurado el `.env`, inicia el lanzador unificado que arrancará simultáneamente el agente de monitoreo y el servidor web:

```bash
python run_cbas.py
```
*Verás mensajes en la terminal confirmando que el servidor web y el agente están en línea y escuchando.*

## Paso 6: Acceso al Panel de Auditoría

Abre tu navegador de internet y dirígete a la siguiente dirección para visualizar la consola de gobernanza y control de versiones:

**[http://127.0.0.1:5050](http://127.0.0.1:5050)**

A partir de este momento, cualquier archivo que crees, modifiques o guardes dentro de `directorio_pyme/` se respaldará y auditará automáticamente en la interfaz web.
