CREATE DATABASE IF NOT EXISTS sgs_infraestructura_db;
USE sgs_infraestructura_db;

CREATE TABLE Salon (
    id_salon INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    capacidad INT NOT NULL,
    estado ENUM('disponible', 'mantenimiento', 'ocupado') DEFAULT 'disponible',
    ubicacion VARCHAR(100)
);