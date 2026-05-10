from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey


from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "tarea2"

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Miembro(Base):

    __tablename__ = "miembro"

    id = Column(Integer, primary_key=True, autoincrement=True)

    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)

    correo = Column(String(100), nullable=False)

    telefono = Column(String(20), nullable=False)

    tipo_miembro = Column(String(30), nullable=False)

    observaciones = Column(Text, nullable=True)

    fecha_registro = Column(
        DateTime,
        nullable=False,
        default=datetime.now
    )

    # PREGRADO
    carrera = Column(String(100), nullable=True)
    ingreso_pregrado = Column(Integer, nullable=True)
    semestre = Column(Integer, nullable=True)

    # POSTGRADO
    programa = Column(String(100), nullable=True)
    grado = Column(String(50), nullable=True)
    ingreso_postgrado = Column(Integer, nullable=True)

    # FUNCIONARIO
    unidad_funcionario = Column(String(100), nullable=True)
    cargo_funcionario = Column(String(100), nullable=True)

    # ACADEMICO
    unidad_academico = Column(String(100), nullable=True)
    cargo_academico = Column(String(100), nullable=True)
    oficina = Column(String(100), nullable=True)

    actividades = relationship(
        "Actividad",
        back_populates="miembro",
        cascade="all, delete"
    )

class Actividad(Base):

    __tablename__ = "actividad"

    id = Column(Integer, primary_key=True, autoincrement=True)

    nombre = Column(String(150), nullable=False)

    descripcion = Column(Text, nullable=False)

    tipo = Column(String(50), nullable=False)

    dias = Column(String(100), nullable=False)

    hora_inicio = Column(String(10), nullable=False)

    hora_termino = Column(String(10), nullable=False)

    enlace = Column(String(300), nullable=False)

    miembro_id = Column(
        Integer,
        ForeignKey("miembro.id"),
        nullable=False
    )

    miembro = relationship(
        "Miembro",
        back_populates="actividades"
    )

    fotos = relationship(
        "Foto",
        back_populates="actividad",
        cascade="all, delete"
    )

class Foto(Base):

    __tablename__ = "foto"

    id = Column(Integer, primary_key=True, autoincrement=True)

    ruta_archivo = Column(String(300), nullable=False)

    actividad_id = Column(
        Integer,
        ForeignKey("actividad.id"),
        nullable=False
    )

    actividad = relationship(
        "Actividad",
        back_populates="fotos"
    )

def init_db():
    Base.metadata.create_all(bind=engine)

def get_ultimos_miembros(limit=5):
    session = SessionLocal()
    miembros = session.query(Miembro).order_by(Miembro.fecha_registro.desc()).limit(limit).all()
    session.close()
    return miembros


def crear_miembro(nombre, email):
    session = SessionLocal()
    nuevo = Miembro(
        nombre=nombre,
        email=email,
        fecha_registro=datetime.now()
    )
    session.add(nuevo)
    session.commit()
    session.close()