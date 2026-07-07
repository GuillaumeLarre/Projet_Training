from database.exercices_repository import ajouter_exercice, charger_catalogue
from database.engine import init_db, SessionLocal


def creer_catalogue():

    init_db()
    with SessionLocal() as session:

        catalogue_existant = charger_catalogue(session)
        if catalogue_existant:
            print("⚠️ Le catalogue contient déjà des exercices. Supprime la base avant de relancer.")
            return
    
        ajouter_exercice(
        session,
        id_exercice="DC01",
        nom="Développé couché haltères",
        groupe_musculaire="pectoraux",
        type_materiel="haltères",
        muscles_cibles=["portion médiane des pecs", "triceps", "deltoide antérieur"]
    )
        ajouter_exercice(
        session,
        id_exercice="DI01",
        nom="Développé incliné haltères",
        groupe_musculaire="pectoraux",
        type_materiel="haltères",
        muscles_cibles=["portion supérieure des pecs", "deltoide antérieur", "triceps"]
    )
        ajouter_exercice(
        session,
        id_exercice="EP01",
        nom="Écartés poulie sur banc incliné 45°",
        groupe_musculaire="pectoraux",
        type_materiel="poulie",
        muscles_cibles=["portion supérieure des pecs", "portion médiane des pecs"]
    )
        ajouter_exercice(
        session,
        id_exercice="CP01",
        nom="Curl pupitre machine",
        groupe_musculaire="bras",
        type_materiel="machine",
        muscles_cibles=["biceps"]
    )
        ajouter_exercice(
        session,
        id_exercice="CU01",
        nom="Curl unilatéral poulie",
        groupe_musculaire="bras",
        type_materiel="poulie",
        muscles_cibles=["biceps"]
    )
        ajouter_exercice(
        session,
        id_exercice="EL01",
        nom="Élévations latérales poulie",
        groupe_musculaire="epaules",
        type_materiel="poulie",
        muscles_cibles=["deltoide médian"]
    )
        ajouter_exercice(
        session,
        id_exercice="EA01",
        nom="Élévations arrière poulie au sol",
        groupe_musculaire="epaules",
        type_materiel="poulie",
        muscles_cibles=["deltoide postérieur"]
    )
        ajouter_exercice(
        session,
        id_exercice="LE01",
        nom="Leg extension machine",
        groupe_musculaire="jambes",
        type_materiel="machine",
        muscles_cibles=["quadriceps"]
    )
        ajouter_exercice(
        session,
        id_exercice="HS01",
        nom="Hack squat machine",
        groupe_musculaire="jambes",
        type_materiel="machine",
        muscles_cibles=["quadriceps", "fessier", "ischios"]
    )
        ajouter_exercice(
        session,
        id_exercice="PR01",
        nom="Presse inclinée 45°",
        groupe_musculaire="jambes",
        type_materiel="machine",
        muscles_cibles=["quadriceps", "fessier", "ischios"]
    )
        ajouter_exercice(
        session,
        id_exercice="LC01",
        nom="Leg curl allongé machine",
        groupe_musculaire="jambes",  
        type_materiel="machine",
        muscles_cibles=["ischios"]
    )
        ajouter_exercice(
        session,
        id_exercice="LA01",
        nom="Leg curl assis machine",
        groupe_musculaire="jambes",  
        type_materiel="machine",
        muscles_cibles=["ischios"]
    )
        ajouter_exercice(
        session,
        id_exercice="AD01",
        nom="Adducteurs machine",
        groupe_musculaire="jambes",
        type_materiel="machine",
        muscles_cibles=["adducteur"]
    )
        ajouter_exercice(
        session,
        id_exercice="RV01",
        nom="Rowing assis poulie basse poignée en V",
        groupe_musculaire="dos",
        type_materiel="poulie",
        muscles_cibles=["grand dorsal", "grand rond", "biceps"]
    )
        ajouter_exercice(
        session,
        id_exercice="TV01",
        nom="Tirage vertical prise neutre",
        groupe_musculaire="dos",
        type_materiel="machine",
        muscles_cibles=["grand dorsal", "grand rond", "biceps"]
    )
        ajouter_exercice(
        session,
        id_exercice="PO01",
        nom="Pull-over poulie haute",
        groupe_musculaire="dos",
        type_materiel="poulie",
        muscles_cibles=["grand dorsal"]
    )
        ajouter_exercice(
        session,
        id_exercice="RM01",
        nom="Rowing machine",
        groupe_musculaire="dos",
        type_materiel="machine",
        muscles_cibles=["trapèze", "grand dorsal", "grand rond"]
    )
        ajouter_exercice(
        session,
        id_exercice="TD01",
        nom="Triceps dips machine",
        groupe_musculaire="bras",
        type_materiel="machine",
        muscles_cibles=["triceps"]
    )
        ajouter_exercice(
        session,
        id_exercice="TE01",
        nom="Extension triceps nuque poulie",
        groupe_musculaire="bras",
        type_materiel="poulie",
        muscles_cibles=["triceps"]
    )
        ajouter_exercice(
        session,
        id_exercice="FS01",
        nom="Fentes statiques haltères",
        groupe_musculaire="jambes",
        type_materiel="haltères",
        muscles_cibles=["quadriceps", "fessier", "ischios"]
    )
        catalogue = charger_catalogue(session)        
        print(f"Catalogue crée : {len(catalogue)} exercices")

if __name__ == "__main__":
    creer_catalogue()