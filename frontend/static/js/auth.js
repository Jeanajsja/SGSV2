import { ROLES_MAP, ROLES } from './config.js';

export function obtenerUsuarioActual() {
    try {
        const user = sessionStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    } catch (e) {
        return null;
    }
}

export function verificarAutenticacion() {
    const user = obtenerUsuarioActual();
    if (!user) {
        window.location.href = 'login.html';
        return null;
    }
    return user;
}

export function aplicarControlRoles(user) {
    const displayName = document.getElementById('user-display-name');
    const displayRole = document.getElementById('user-display-role');

    if (displayName) displayName.innerText = user.nombre;
    if (displayRole) displayRole.innerText = ROLES_MAP[user.id_rol] || 'DESCONOCIDO';

    const rol = parseInt(user.id_rol);
    
    // DOCENTE: No ve Docentes, Reservas Globales ni Roles
    if (rol === ROLES.DOCENTE) {
        ['nav-docentes', 'nav-reservas', 'nav-roles'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.style.display = 'none';
        });
        const seccionGrafico = document.getElementById('seccion-grafico');
        if (seccionGrafico) seccionGrafico.style.display = 'none';
    } 
    // OPERATIVO: No ve Control de Roles
    else if (rol === ROLES.OPERATIVO) {
        const el = document.getElementById('nav-roles');
        if (el) el.style.display = 'none';
    }
}

export function cerrarSesion() {
    sessionStorage.clear();
    window.location.href = 'login.html';
}