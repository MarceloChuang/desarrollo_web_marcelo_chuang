from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
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

class Comentario(Base):
    __tablename__ = "comentario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)
    texto = Column(Text, nullable=False)
    fecha = Column(DateTime, nullable=False, default=datetime.now)
    actividad_id = Column(Integer, ForeignKey("actividad.id"), nullable=False)
    actividad = relationship("Actividad", back_populates="comentarios")

class Region(Base):
    __tablename__ = "region"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)

    comunas = relationship("Comuna", back_populates="region")


class Comuna(Base):
    __tablename__ = "comuna"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)

    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)

    region = relationship("Region", back_populates="comunas")
    miembros = relationship("Miembro", back_populates="comuna")

class Miembro(Base):
    __tablename__ = "miembro"

    id = Column(Integer, primary_key=True, autoincrement=True)

    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    tipo_miembro = Column(String(30), nullable=False)
    comuna_id = Column(Integer, ForeignKey("comuna.id"), nullable=False)
    comuna = relationship("Comuna", back_populates="miembros")

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
    comentarios = relationship(
        "Comentario",
        back_populates="actividad",
        cascade="all, delete"
    )
    notas = relationship(
        "Nota",
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


class Nota(Base):
    __tablename__ = "nota"

    id = Column(Integer, primary_key=True, autoincrement=True)

    valor = Column(Integer, nullable=False)

    actividad_id = Column(
        Integer,
        ForeignKey("actividad.id"),
        nullable=False
    )

    fecha = Column(DateTime, nullable=False, default=datetime.now)

    actividad = relationship(
        "Actividad",
        back_populates="notas"
    )
    

def init_db():
    Base.metadata.create_all(bind=engine)


def get_ultimos_miembros(limit=5):
    session = SessionLocal()

    miembros = (
        session.query(Miembro)
        .options(joinedload(Miembro.comuna))
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
        .options(joinedload(Miembro.comuna))
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
    comuna_id,
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
        comuna_id=comuna_id,
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

def crear_comentario(actividad_id, nombre, texto):
    session = SessionLocal()

    comentario = Comentario(
        actividad_id=actividad_id,
        nombre=nombre,
        texto=texto,
        fecha=datetime.now()
    )

    session.add(comentario)
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


def get_miembro_by_id(miembro_id):
    session = SessionLocal()

    miembro = (
        session.query(Miembro)
        .options(joinedload(Miembro.comuna))
        .options(joinedload(Miembro.actividades).joinedload(Actividad.fotos))
        .filter(Miembro.id == miembro_id)
        .first()
    )

    session.close()
    return miembro

def get_todas_comunas():
    session = SessionLocal()

    comunas = (
        session.query(Comuna)
        .order_by(Comuna.nombre.asc())
        .all()
    )

    session.close()
    return comunas

def estadistica_miembros_por_dia():
    session = SessionLocal()

    resultados = (
        session.query(
            func.date(Miembro.fecha_registro).label("fecha"),
            func.count(Miembro.id).label("total")
        )
        .group_by(func.date(Miembro.fecha_registro))
        .order_by(func.date(Miembro.fecha_registro))
        .all()
    )

    session.close()

    return [{"fecha": str(fecha),"total": total} for fecha, total in resultados]

def estadistica_actividades_por_tipo():
    session = SessionLocal()

    resultados = (
        session.query(
            Actividad.tipo,
            func.count(Actividad.id).label("total")
        )
        .group_by(Actividad.tipo)
        .order_by(Actividad.tipo)
        .all()
    )

    session.close()

    return [{"tipo": tipo,"total": total} for tipo, total in resultados]


def estadistica_actividades_por_comuna():
    session = SessionLocal()

    resultados = (
        session.query(
            Comuna.nombre,
            func.count(Actividad.id).label("total")
        )
        .join(Miembro, Miembro.comuna_id == Comuna.id)
        .join(Actividad, Actividad.miembro_id == Miembro.id)
        .group_by(Comuna.id, Comuna.nombre)
        .order_by(Comuna.nombre)
        .all()
    )

    session.close()

    return [{"comuna": comuna,"total": total} for comuna, total in resultados]

def get_comentarios_actividad(actividad_id):
    session = SessionLocal()

    comentarios = (
        session.query(Comentario)
        .filter(Comentario.actividad_id == actividad_id)
        .order_by(Comentario.fecha.desc())
        .all()
    )

    session.close()

    return comentarios

def get_actividad_by_id(actividad_id):
    session = SessionLocal()

    actividad = (
        session.query(Actividad)
        .options(
            joinedload(Actividad.miembro).joinedload(Miembro.comuna),
            joinedload(Actividad.fotos),
            joinedload(Actividad.comentarios)
        )
        .filter(Actividad.id == actividad_id)
        .first()
    )

    session.close()
    return actividad
