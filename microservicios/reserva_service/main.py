import os
import sys
from flask import Flask
from flask_cors import CORS

# Configurar el PATH para que pueda importar módulos locales
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
# Habilitar CORS para permitir solicitudes del API Gateway o Frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Importar y Registrar Controladores (Blueprints)
from controllers.reserva_controller import reserva_bp

app.register_blueprint(reserva_bp, url_prefix='/api')

if __name__ == '__main__':
    # El microservicio de Reservas (Core) corre en el puerto 5004
    print("Iniciando Reserva Service en el puerto 5004...")
    app.run(host='0.0.0.0', port=5004, debug=True)
