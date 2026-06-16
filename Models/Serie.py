import logging
logger = logging.getLogger(__name__)

class Serie:
    def __init__(self, poids: float, reps: int, est_echauffement: bool = False) -> None:
        if poids <= 0 or reps <= 0:
            logger.warning(f"Création de Série refusée : poids={poids}, reps={reps}")
            raise ValueError("valeur incorrecte")
        self.poids = poids
        self.reps = reps
        self.est_echauffement = est_echauffement

    @property
    def volume(self) -> float:
        return round((self.poids * self.reps), 1)
    
    def __str__(self) -> str:
        return f"{self.poids:.1f} kg x {self.reps}"
    
    def to_dict(self) -> dict:
        return {"poids": self.poids, "reps": self.reps, "est_echauffement": self.est_echauffement}
    
    @classmethod
    def from_dict(cls, donnees: dict) -> "Serie":
        est_echauffement = donnees.get("est_echauffement", False)
        return cls(donnees["poids"], donnees["reps"], est_echauffement)