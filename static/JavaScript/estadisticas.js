document.addEventListener("DOMContentLoaded", () => {
    cargarGraficoMiembrosPorDia();
    cargarGraficoActividadesPorTipo();
    cargarGraficoActividadesPorComuna();
});

async function cargarGraficoMiembrosPorDia() {
    try {
        const response = await fetch("/api/estadisticas/miembros-por-dia");
        const datos = await response.json();

        Highcharts.chart("grafico-miembros-dia", {
            chart: {type: "line"},
            title: {text: "Cantidad de miembros registrados por día"},
            xAxis: {categories: datos.map(item => item.fecha), title: {text: "Día"}},
            yAxis: {title: {text: "Cantidad de miembros"}, allowDecimals: false},
            series: [{name: "Miembros", data: datos.map(item => item.total)}]
        });
    } catch (error) {
        console.error("Error cargando gráfico de miembros por día:", error);
    }
}

async function cargarGraficoActividadesPorTipo() {
    try {
        const response = await fetch("/api/estadisticas/actividades-por-tipo");
        const datos = await response.json();

        Highcharts.chart("grafico-actividades-tipo", {
            chart: {type: "pie"},
            title: {text: "Total de actividades por tipo"},
            tooltip: {pointFormat: "<b>{point.y}</b> actividades"},
            series: [{name: "Actividades", colorByPoint: true, data: datos.map(item => ({name: item.tipo, y: item.total}))}]
        });
    } catch (error) {
        console.error("Error cargando gráfico de actividades por tipo:", error);
    }
}

async function cargarGraficoActividadesPorComuna() {
    try {
        const response = await fetch("/api/estadisticas/actividades-por-comuna");
        const datos = await response.json();

        Highcharts.chart("grafico-actividades-comuna", {
            chart: {type: "column"},
            title: {text: "Total de actividades registradas por comuna"},
            yAxis: {title: { text: "Total de actividades" }, allowDecimals: false},
            xAxis: {categories: datos.map(item => item.comuna), title: {text: "Comuna"}},
            series: [{name: "Actividades", data: datos.map(item => item.total)}]});
    } catch (error) {
        console.error("Error cargando gráfico de actividades por comuna:", error);
    }
}