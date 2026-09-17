from flask import Flask, request, Response
import requests

app = Flask(__name__)

# =====================================================================
# FEATURE TOGGLES (BRANCH BY ABSTRACTION / BLUE-GREEN DEPLOYMENT)
# =====================================================================
# True = GREEN (Nuevo Microservicio)
# False = BLUE (Monolito Antiguo)
TOGGLES = {
    "auth": False,      # Monolito
    "salones": False,   # Monolito
    "docentes": False,  # Monolito
    "reservas": True    # ¡NUEVO MICROSERVICIO ACTIVADO!
}

# =====================================================================
# RUTAS DE LOS SERVICIOS
# =====================================================================
# El Monolito (BLUE) ahora debe correr en el puerto 5555
MONOLITH_URL = "http://localhost:5555/api"

# Microservicios (GREEN)
MICROSERVICES = {
    "auth": "http://localhost:5001/api",
    "salones": "http://localhost:5002/api",
    "docentes": "http://localhost:5003/api",
    "reservas": "http://localhost:5004/api"
}

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # Identificar el dominio según la primera parte de la URL
    domain = path.split('/')[0]
    
    # Mapeo de rutas legacy al dominio 'auth'
    if domain in ['login', 'usuarios', 'roles']: 
        domain = 'auth'

    # BRANCH BY ABSTRACTION: Decidir a dónde enviar el tráfico
    use_new_service = TOGGLES.get(domain, False)
    
    if use_new_service:
        target_base_url = MICROSERVICES.get(domain)
        print(f"[GREEN] Enrutando '{domain}' al Microservicio -> {target_base_url}")
    else:
        target_base_url = MONOLITH_URL
        print(f"[BLUE] Enrutando '{domain}' al Monolito -> {target_base_url}")

    if not target_base_url: 
        return {"error": "Servicio no encontrado"}, 404

    # Reconstruir la URL de destino
    url = f"{target_base_url}/{path}"
    
    try:
        # Enviar la petición interceptada al destino elegido (Blue o Green)
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        return Response(resp.content, resp.status_code, resp.headers.items())
    except requests.exceptions.ConnectionError:
        return {"error": f"No se pudo conectar al servicio en {url}. ¿Está encendido?"}, 503

if __name__ == '__main__':
    # El API Gateway SE APODERA del puerto 5000 (donde antes vivía el monolito)
    print("Iniciando API Gateway (Branch by Abstraction) en el puerto 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
