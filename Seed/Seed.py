import os
import sys
from Models.Exercice import Exercice
from Models.CarnetEntrainement import CarnetEntrainement


def creer_catalogue():

    if os.path.exists("carnet.json"):
        print("⚠️  carnet.json existe déjà. Supprime-le manuellement avant de relancer ce script.")
        sys.exit()
    
    carnet = CarnetEntrainement()
    
    carnet.ajouter_exercice(Exercice(
    id_exercice="DC01",
    nom="Développé couché haltères",
    groupe_musculaire="pectoraux",
    muscle_cible=["portion médiane des pecs", "triceps", "deltoide antérieur"],
    type_materiel="haltères",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="DI01",
    nom="Développé incliné haltères",
    groupe_musculaire="pectoraux",
    muscle_cible=["portion supérieure des pecs", "deltoide antérieur", "triceps"],
    type_materiel="haltères",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="EP01",
    nom="Écartés poulie sur banc incliné 45°",
    groupe_musculaire="pectoraux",
    muscle_cible=["portion supérieure des pecs", "portion médiane des pecs"],
    type_materiel="poulie",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="CP01",
    nom="Curl pupitre machine",
    groupe_musculaire="bras",
    muscle_cible=["biceps"],
    type_materiel="machine",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="CU01",
    nom="Curl unilatéral poulie",
    groupe_musculaire="bras",
    muscle_cible=["biceps"],
    type_materiel="poulie",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="EL01",
    nom="Élévations latérales haltères",
    groupe_musculaire="epaules",
    muscle_cible=["deltoide médian"],
    type_materiel="haltères",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="EA01",
    nom="Élévations arrière poulie au sol (à genoux)",
    groupe_musculaire="epaules",
    muscle_cible=["deltoide postérieur"],
    type_materiel="poulie",
))
    carnet.ajouter_exercice(Exercice(
    id_exercice="LE01",
    nom="Leg extension machine",
    groupe_musculaire="jambes",
    muscle_cible=["quadriceps"],
    type_materiel="machine",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="HS01",
    nom="Hack squat machine",
    groupe_musculaire="jambes",
    muscle_cible=["quadriceps", "fessier", "ischios"],
    type_materiel="machine",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="PR01",
    nom="Presse inclinée 45°",
    groupe_musculaire="jambes",
    muscle_cible=["quadriceps", "fessier", "ischios"],
    type_materiel="machine",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="LC01",
    nom="Leg curl allongé machine",
    groupe_musculaire="jambes",
    muscle_cible=["ischios"],   # à confirmer
    type_materiel="machine",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="LA01",
    nom="Leg curl assis machine",
    groupe_musculaire="jambes",
    muscle_cible=["ischios"],   # à confirmer
    type_materiel="machine",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="AD01",
    nom="Adducteurs machine",
    groupe_musculaire="jambes",
    muscle_cible=["adducteur"],
    type_materiel="machine",
))
    carnet.ajouter_exercice(Exercice(
    id_exercice="RV01",
    nom="Rowing assis poulie basse poignée en V",
    groupe_musculaire="dos",
    muscle_cible=["grand dorsal", "grand rond", "biceps"],
    type_materiel="poulie",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="TV01",
    nom="Tirage vertical prise neutre largeur épaules",
    groupe_musculaire="dos",
    muscle_cible=["grand dorsal", "grand rond", "biceps"],
    type_materiel="machine",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="PO01",
    nom="Pull-over poulie haute (straight-arm pulldown)",
    groupe_musculaire="dos",
    muscle_cible=["grand dorsal"],
    type_materiel="poulie",
))

    carnet.ajouter_exercice(Exercice(
    id_exercice="RM01",
    nom="Rowing machine appui poitrine, coudes larges",
    groupe_musculaire="dos",
    muscle_cible=["trapèze", "grand dorsal", "grand rond"],
    type_materiel="machine",
))

    

    carnet.sauvegarder("carnet.json")
    print(f"Catalogue créé : {len(carnet.exercices)} exercices.")


if __name__ == "__main__":
    creer_catalogue()