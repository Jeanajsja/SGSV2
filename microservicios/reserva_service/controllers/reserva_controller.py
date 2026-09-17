from flask import Blueprint, request, jsonify, Response
from services.reserva_service import ReservaService
from typing import Tuple

reserva_bp = Blueprint('reserva', __name__)
service = ReservaService()

@reserva_bp.route('/reservas', methods=['GET'])
def listar() -> Tuple[Response, int]:
    """Obtiene la lista de reservas filtrada por usuario y rol."""
    try:
        raw_id_usuario = request.headers.get('X-User-Id') or request.args.get('id_usuario')
        raw_id_rol = request.headers.get('X-Rol-Id') or request.args.get('id_rol')
        
        # Conversión segura a entero evitando ValueError si envían texto basura
        id_usuario = int(raw_id_usuario) if raw_id_usuario and str(raw_id_usuario).isdigit() else None
        id_rol = int(raw_id_rol) if raw_id_rol and str(raw_id_rol).isdigit() else None
        
        resultado = service.listar(id_usuario, id_rol)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al listar reservas: {str(e)}"}), 400

@reserva_bp.route('/reservas/estadisticas', methods=['GET'])
def estadisticas() -> Tuple[Response, int]:
    """Obtiene las estadísticas agrupadas de reservas desde el servidor."""
    try:
        resultado = service.obtener_estadisticas()
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al obtener estadísticas: {str(e)}"}), 500

@reserva_bp.route('/reservas', methods=['POST'])
def crear() -> Tuple[Response, int]:
    """Crea una reserva nueva o la ingresa a la cola de espera."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "El cuerpo de la petición debe ser un JSON válido."}), 400
        
    respuesta = service.crear_reserva(data)
    # Si se crea con éxito o va a cola, retornamos código 201 (Created), de lo contrario 400
    status_code = 201 if respuesta.get("status") in ("ok", "cola") else 400
    return jsonify(respuesta), status_code

@reserva_bp.route('/reservas/<int:id_reserva>', methods=['PUT'])
def actualizar(id_reserva: int) -> Tuple[Response, int]:
    """Actualiza una reserva existente."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "El cuerpo de la petición debe ser un JSON válido."}), 400
        
    respuesta = service.actualizar_reserva(id_reserva, data)
    status_code = 200 if respuesta.get("status") == "ok" else 400
    return jsonify(respuesta), status_code

@reserva_bp.route('/reservas/<int:id_reserva>', methods=['DELETE'])
def cancelar(id_reserva: int) -> Tuple[Response, int]:
    """Cancela una reserva y activa la notificación al siguiente en cola."""
    respuesta = service.cancelar_reserva(id_reserva)
    status_code = 200 if respuesta.get("status") == "ok" else 400
    return jsonify(respuesta), status_code