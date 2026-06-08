INSERT INTO actividad (
    nombre,
    descripcion,
    tipo,
    dias,
    hora_inicio,
    hora_termino,
    enlace,
    miembro_id
)
VALUES
(
    'Club Hearthstone',
    'Partidas semanales',
    'recreativa',
    'sabado',
    '20:00',
    '22:00',
    'https://youtube.com',
    1
),
(
    'Hackathon',
    'Programacion competitiva',
    'tecnologica',
    'viernes',
    '18:00',
    '23:00',
    'https://github.com',
    1
),
(
    'Seminario IA',
    'Charla de inteligencia artificial',
    'academica',
    'miercoles',
    '15:00',
    '17:00',
    'https://openai.com',
    2
),
(
    'Futbol DCC',
    'Actividad deportiva',
    'deportiva',
    'domingo',
    '10:00',
    '12:00',
    'https://uach.cl',
    3
),
(
    'Torneo Ajedrez',
    'Competencia interna',
    'recreativa',
    'jueves',
    '18:00',
    '20:00',
    'https://chess.com',
    5
);