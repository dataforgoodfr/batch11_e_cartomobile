import uuid

from geoalchemy2 import Geometry
from sqlalchemy import UUID, Boolean, Column, DateTime, Float, Integer, String

from e_cartomobile.infra.database.database_manager import Base


class Communes(Base):
    __tablename__ = "communes"
    insee = Column("insee", String, primary_key=True, index=True)
    nom_commune = Column(String)
    surf_ha = Column(Float)
    geometry = Geometry("GEOMETRY")
    

class Score4(Base):
    __tablename__ = "score4"
    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    last_update = Column("last_update", DateTime)
    gamma = Column("gamma", Float)
    max_distance_km = Column("max_distance_km", Float)
    insee = Column("insee", String, index=True)
    score_4 = Column("score_4", Float)
 
