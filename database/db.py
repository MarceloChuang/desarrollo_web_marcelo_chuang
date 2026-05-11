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

    fecha_registro = Column(DateTime, nullable=False, default=datetime.now)

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

    miembro_id = Column(Integer, ForeignKey("miembro.id"), nullable=False)

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
    nombre_archivo = Column(String(300), nullable=False)

    actividad_id = Column(Integer, ForeignKey("actividad.id"), nullable=False)

    actividad = relationship(
        "Actividad",
        back_populates="fotos"
    )


def init_db():
    Base.metadata.create_all(bind=engine)


def get_ultimos_miembros(limit=5):
    session = SessionLocal()

    miembros = (
        session.query(Miembro)
        .order_by(Miembro.fecha_registro.desc())
        .limit(limit)
        .all()
    )

    session.close()
    return miembros


def get_miembros_paginados(page=1, per_page=5):
    session = SessionLocal()

    offset = (page - 1) * per_page

    miembros = (
        session.query(Miembro)
        .order_by(Miembro.fecha_registro.desc())
        .offset(offset)
        .limit(per_page)
        .all()
    )

    total = session.query(Miembro).count()

    session.close()
    return miembros, total


def get_miembro_by_id(miembro_id):
    session = SessionLocal()

    miembro = (
        session.query(Miembro)
        .filter(Miembro.id == miembro_id)
        .first()
    )

    session.close()
    return miembro


def crear_miembro(
    nombres,
    apellidos,
    correo,
    telefono,
    tipo_miembro,
    observaciones=None,
    carrera=None,
    ingreso_pregrado=None,
    semestre=None,
    programa=None,
    grado=None,
    ingreso_postgrado=None,
    unidad_funcionario=None,
    cargo_funcionario=None,
    unidad_academico=None,
    cargo_academico=None,
    oficina=None
):
    session = SessionLocal()

    nuevo = Miembro(
        nombres=nombres,
        apellidos=apellidos,
        correo=correo,
        telefono=telefono,
        tipo_miembro=tipo_miembro,
        observaciones=observaciones,
        carrera=carrera,
        ingreso_pregrado=ingreso_pregrado,
        semestre=semestre,
        programa=programa,
        grado=grado,
        ingreso_postgrado=ingreso_postgrado,
        unidad_funcionario=unidad_funcionario,
        cargo_funcionario=cargo_funcionario,
        unidad_academico=unidad_academico,
        cargo_academico=cargo_academico,
        oficina=oficina,
        fecha_registro=datetime.now()
    )

    session.add(nuevo)
    session.commit()

    miembro_id = nuevo.id

    session.close()

    return miembro_id


def crear_actividad(
    miembro_id,
    nombre,
    descripcion,
    tipo,
    dias,
    hora_inicio,
    hora_termino,
    enlace
):
    session = SessionLocal()

    nueva = Actividad(
        miembro_id=miembro_id,
        nombre=nombre,
        descripcion=descripcion,
        tipo=tipo,
        dias=dias,
        hora_inicio=hora_inicio,
        hora_termino=hora_termino,
        enlace=enlace
    )

    session.add(nueva)
    session.commit()

    actividad_id = nueva.id

    session.close()

    return actividad_id


def crear_foto(ruta_archivo, nombre_archivo, actividad_id):
    session = SessionLocal()

    nueva = Foto(
        ruta_archivo=ruta_archivo,
        nombre_archivo=nombre_archivo,
        actividad_id=actividad_id
    )

    session.add(nueva)
    session.commit()

    session.close()

def get_todos_miembros():
    session = SessionLocal()

    miembros = (
        session.query(Miembro)
        .order_by(Miembro.nombres.asc(), Miembro.apellidos.asc())
        .all()
    )

    session.close()
    return miembros