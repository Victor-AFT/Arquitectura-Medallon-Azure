import azure.functions as func
import logging
import requests
from urllib.parse import urlparse
from os.path import basename
import os
import json
from datetime import datetime, timedelta, timezone
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="GetFlights")
@app.route(route="GetFlights", methods=[func.HttpMethod.GET])

def GetFlights(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("GET /api/GetFlights - llamando a Aviationstack")

    #Variables desde local.settings.json
    api_key = os.environ["AVIATIONSTACK_API_KEY"]
    url = os.environ["url"]

    params = {
        "access_key": api_key
    }

    # 1) Llamada a la API REST
    try:
        r = requests.get(url, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        logging.info("GET /api/GetFlights - Descarga correcta.")
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(f"Error llamando a Aviationstack: {str(e)}", status_code=500)

    # 2) Subir JSON a Azure Blob Storage
    try:
        conn_str = os.environ["AzureStorageEndpoint"]
        blob_service = BlobServiceClient.from_connection_string(conn_str)

        container_name = os.environ["container"]
        container = blob_service.get_container_client(container_name)

        # Crear contenedor si no existe
        try:
            container.create_container()
        except Exception:
            pass

        # Ruta tipo Medallion Bronze
        now = datetime.utcnow()
        timestamp = now.strftime("%Y%m%d%H%M%S")

        blob_name = (
            f"flights_{timestamp}.json"
        )

        blob_client = container.get_blob_client(blob=blob_name)

        #Guarda JSON formateado
        blob_client.upload_blob(
            json.dumps(data, ensure_ascii=False, indent=2),
            overwrite=True
        )

        logging.info(f"Archivo guardado: {blob_name}")

        # 3) Generar SAS URL (1 hora)
        sas = generate_blob_sas(
            account_name=blob_service.account_name,
            container_name=container_name,
            blob_name=blob_name,
            account_key=blob_service.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now(timezone.utc) + timedelta(hours=1)
        )

        sas_url = f"https://{blob_service.account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas}"

    except Exception as e:
        logging.error(e)
        return func.HttpResponse(f"Error subiendo a Blob Storage: {str(e)}", status_code=500)

    # 4) Respuesta final
    return func.HttpResponse(
        json.dumps({
            "ok": True,
            "blob_name": blob_name,
            "sas_url": sas_url,
            "records": len(data.get("data", []))
        }, ensure_ascii=False),
        status_code=200,
        mimetype="application/json"
    )