from Fonctions_utiles.fonctions import accord
from Models.Serie import Serie

class ExerciceRealise:
    def __init__(self, exercice):
        self.exercice = exercice
        self.series = []

    def ajouter_serie(self, serie):
        self.series.append(serie)

    @property
    def volume_total(self):
        return sum(s.volume for s in self.series)

    @property
    def nb_series(self):
        return len(self.series)

    @property
    def serie_plus_lourde(self):
        if self.series == []:
            return None
        else:   
            top_serie = sorted(self.series, key=lambda s: s.poids, reverse=True)[0]
            return top_serie
        

    def __str__(self):
        return f"{self.exercice} - {self.nb_series} {accord(self.nb_series, 'série', 'séries')}, volume : {self.volume_total:.1f} kg"

    def to_dict(self):
        return {"id_exercice": self.exercice.id_exercice, "series": [s.to_dict() for s in self.series]}
    
    @classmethod
    def from_dict(cls, donnees, catalogue_exercices):
        exercice = catalogue_exercices[donnees["id_exercice"]]
        exercice_realise = cls(exercice)
        for s_dict in donnees["series"]:
            serie = Serie.from_dict(s_dict)
            exercice_realise.ajouter_serie(serie)
        return exercice_realise