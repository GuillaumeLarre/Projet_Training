from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint

class Base(DeclarativeBase):
    pass

class Exercice(Base):
    __tablename__ = "exercices"
    id_exercice: Mapped[str] = mapped_column(primary_key=True)
    nom: Mapped[str]
    groupe_musculaire: Mapped[str]
    type_materiel: Mapped[str]

class MuscleCibleExercice(Base):
    __tablename__ = "muscles_cibles_exercices"
    id_exercice: Mapped[str] = mapped_column(ForeignKey("exercices.id_exercice"), primary_key=True)
    nom_muscle: Mapped[str] = mapped_column(primary_key=True)

class Seance(Base):
    __tablename__ = "seances"
    id_seance: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(unique=True)
    duree: Mapped[int] = mapped_column(CheckConstraint("duree > 0"))

class ExerciceRealise(Base):
    __tablename__ = "exercices_realises"
    id_exercice_realise: Mapped[int] = mapped_column(primary_key=True)
    id_exercice: Mapped[str] = mapped_column(ForeignKey("exercices.id_exercice"))
    id_seance: Mapped[int] = mapped_column(ForeignKey("seances.id_seance", ondelete="CASCADE"))
    __table_args__ = (
        UniqueConstraint("id_seance", "id_exercice"),
    )

class Serie(Base):
    __tablename__ = "series"
    id_serie: Mapped[int] = mapped_column(primary_key=True)
    numero_serie: Mapped[int]
    poids: Mapped[float] = mapped_column(CheckConstraint("poids > 0"))
    reps: Mapped[int] = mapped_column(CheckConstraint("reps > 0"))
    est_echauffement: Mapped[bool] = mapped_column(CheckConstraint("est_echauffement IN (0, 1)"), default=False)
    id_exercice_realise: Mapped[int] = mapped_column(ForeignKey("exercices_realises.id_exercice_realise", ondelete="CASCADE"))
    __table_args__ = (
        UniqueConstraint("id_exercice_realise", "numero_serie"),
    )