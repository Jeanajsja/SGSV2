from flask import Blueprint, request, jsonify
from services.reserva_service import ReservaService

reserva_bp = Blueprint('reserva', __name__)
service = ReservaService()

@reserva_bp.route('/reservas', methods=['GET'])
def listar():
    # En un entorno real, estos vendrían de un Token JWT decodificado en un Middleware.
    # Para fines del taller, los pasamos por headers o query params.
    id_usuario = request.headers.get('X-User-Id') or request.args.get('id_usuario')
    id_rol = request.headers.get('X-Rol-Id') or request.args.get('id_rol')
    
    if id_usuario: id_usuario = int(id_usuario)
    if id_rol: id_rol = int(id_rol)

    return jsonify(service.listar(id_usuario, id_rol))

@reserva_bp.route('/reservas/estadisticas', methods=['GET'])
def estadisticas():
    # Nuevo endpoint para agrupar en el servidor y evitar que el JS lo haga
    return jsonify(service.obtener_estadisticas())

@reserva_bp.route('/reservas', methods=['POST'])
def crear(): 
    return jsonify(service.crear_reserva(request.json))

@reserva_bp.route('/reservas/<int:id>', methods=['PUT'])
def actualizar(id): 
    return jsonify(service.actualizar_reserva(id, request.json))

@reserva_bp.route('/reservas/<int:id>', methods=['DELETE'])
def cancelar(id): 
    return jsonify(service.cancelar_reserva(id))
