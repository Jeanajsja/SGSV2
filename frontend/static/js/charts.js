import { API_URL } from './config.js';

let chartInstance = null;

export async function initChart(user) {
    if (user.id_rol == 3) return; // Docente no tiene permisos del gráfico

    try {
        const res = await fetch(`${API_URL}/reservas`);
        const result = await res.json();
        if (!res.ok || !result.data) return;

        // Agrupar reservas por salón de forma optimizada
        const salonesMap = result.data.reduce((acc, r) => {
            if (r.estado !== 'cancelada') {
                acc[r.salon] = (acc[r.salon] || 0) + 1;
            }
            return acc;
        }, {});

        const labels = Object.keys(salonesMap);
        const data = Object.values(salonesMap);

        const canvas = document.getElementById('reservasChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (chartInstance) {
            chartInstance.destroy();
        }

        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Reservas Activas por Salón',
                    data: data,
                    backgroundColor: 'rgba(37, 99, 235, 0.65)',
                    borderColor: 'rgba(37, 99, 235, 1)',
                    borderWidth: 2,
                    borderRadius: 12,
                    barPercentage: 0.5,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#1e293b',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        padding: 12,
                        cornerRadius: 8,
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8', font: { weight: 'bold' } }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: '#f1f5f9' },
                        ticks: { 
                            color: '#94a3b8', 
                            stepSize: 1,
                            font: { weight: 'bold' }
                        }
                    }
                }
            }
        });
    } catch (e) {
        console.error("Error al graficar reservas:", e);
    }
}