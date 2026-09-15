CREATE DATABASE IF NOT EXISTS sgs_operaciones_db;
USE sgs_operaciones_db;

CREATE TABLE Reserva (
    id_reserva INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado ENUM('confirmada', 'cancelada', 'pendiente_confirmacion') DEFAULT 'pendiente_confirmacion',
    id_docente INT NOT NULL,  -- Referencia lógica a sgs_usuarios_db.Docente(id_docente)
    id_salon INT NOT NULL,    -- Referencia lógica a sgs_infraestructura_db.Salon(id_salon)
    id_operador INT NULL,     -- Referencia lógica a sgs_usuarios_db.Operador(id_operador)
    fecha_notificacion DATETIME NULL
);

CREATE TABLE ColaEspera (
    id_cola INT PRIMARY KEY AUTO_INCREMENT,
    id_salon INT NOT NULL,    -- Referencia lógica a infraestructura
    id_docente INT NOT NULL,  -- Referencia lógica a usuarios
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);