from dropbox import DropboxOAuth2FlowNoRedirect
from cbas.config import DROPBOX_APP_KEY, DROPBOX_APP_SECRET

auth_flow = DropboxOAuth2FlowNoRedirect(
    DROPBOX_APP_KEY, 
    DROPBOX_APP_SECRET, 
    token_access_type='offline'
)

authorize_url = auth_flow.start()
print("1. Abre este enlace en tu navegador:\n" + authorize_url)
print("2. Inicia sesión en Dropbox, autoriza la app y copia el código que te dará.")
auth_code = input("\n3. Pega el código de autorización aquí: ").strip()

try:
    oauth_result = auth_flow.finish(auth_code)
    print("\n¡Éxito! Este es tu Refresh Token definitivo. Cópialo al archivo .env:")
    print(oauth_result.refresh_token)
except Exception as e:
    print(f"Error en la autorización: {e}")