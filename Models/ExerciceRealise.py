from fonctions_utiles.fonctions import accord
from models.Serie import Serie
from models.Exercice import Exercice

class ExerciceRealise:
    def __init__(self, exercice: Exercice) -> None:
        self.exercice = exercice
        self.series: list[Serie] = []

    def ajouter_serie(self, serie: Serie) -> None:
        self.series.append(serie)

    @property
    def volume_total(self) -> float:
        multiplicateur = 2 if self.exercice.type_materiel == "haltères" else 1
        somme_series = sum(s.volume for s in self.series if not s.est_echauffement)
        return round((multiplicateur * somme_series), 1)

    @property
    def nb_series(self) -> int:
        return sum(1 for s in self.series if not s.est_echauffement)

    @property
    def serie_plus_lourde(self) -> Serie | None:
        if self.series == []:
            return None
        else:   
            top_serie = sorted(self.series, key=lambda s: s.poids, reverse=True)[0]
            return top_serie
        

    def __str__(self) -> str:
        return f"{self.exercice} - {self.nb_series} {accord(self.nb_series, 'série', 'séries')}, volume : {self.volume_total:.1f} kg"

    def to_dict(self) -> dict:
        return {"id_exercice": self.exercice.id_exercice, "series": [s.to_dict() for s in self.series]}
    
    @classmethod
    def from_dict(cls, donnees: dict, catalogue_exercices: dict[str, Exercice]) -> "ExerciceRealise":
        exercice = catalogue_exercices[donnees["id_exercice"]]
        exercice_realise = cls(exercice)
        for s_dict in donnees["series"]:
            serie = Serie.from_dict(s_dict)
            exercice_realise.ajouter_serie(serie)
        return exercice_realise