from interface.interface import (afficher_menu, saisir_seance, afficher_records, saisir_exercice, lister_catalogue, supprimer_seances, modifier_seance)

from fonctions_utiles.fonctions import accord, sans_accents

from datetime import date

from stats.stats import (evolution_des_charges_dans_le_temps, lister_exercices_differents_par_groupe, un_rm_estime_par_exercice, nb_series_par_groupe_et_par_muscle_cible_par_semaine, frequence_groupe_et_par_muscle_par_semaine, comparaison_nb_series_par_groupe_et_fourchette_scientifique)

from config_logging import configurer_logging

from interface.interface import afficher_historique

from database.seances_repository import charger_toutes_les_seances_completes
from database.engine import init_db, SessionLocal

import logging
logger = logging.getLogger(__name__)



def lancer_application():
    logger.info("Démarrage de l'application")
    init_db()
    with SessionLocal() as session:
        print("╔═══════════════════════════════════════╗")
        print("║  CARNET D'ENTRAÎNEMENT MUSCULATION    ║")
        print("╚═══════════════════════════════════════╝")
        while True:
            afficher_menu()
            choix = input("Entre ton choix : ")
            if choix == "1":
                saisir_seance(session)
            elif choix == "2":
                afficher_historique(session)
            elif choix == "3":
                lister_catalogue(session)
            elif choix == "4":
                saisir_exercice(session)
            elif choix == "5":
                seances = charger_toutes_les_seances_completes(session)
                if not seances:
                    print("Aucune séance enregistrée")
                    continue
                aujourdhui = date.today()
                annee, num_semaine, jour = aujourdhui.isocalendar()
                print(f"========= Récap semaine {num_semaine}/{annee} =========\n")
                print(f"=== Nombre de séries ===\n")
                print(f"--- Nombre de séries par groupe ---\n")
                nb_series_par_groupe, nb_series_muscles_cible = nb_series_par_groupe_et_par_muscle_cible_par_semaine(seances)
                series_groupe_semaine_en_cours = {cle: valeur for cle, valeur in nb_series_par_groupe.items() if cle[0] == annee and cle[1] == num_semaine}
                series_muscle_semaine_en_cours = {cle: valeur for cle, valeur in nb_series_muscles_cible.items() if cle[0] == annee and cle[1] == num_semaine}
                if not series_groupe_semaine_en_cours:
                    print("Aucune séance cette semaine")
                    continue
                for cle, valeur in sorted(series_groupe_semaine_en_cours.items(), key=lambda p: (p[0][0], p[0][1], sans_accents(p[0][2]))):
                    print(f"- {cle[2]} : {valeur} {accord(valeur, 'série', 'séries')}")
                print()
                print(f"--- Nombre de séries par muscle ---\n")
                for cle, valeur in sorted(series_muscle_semaine_en_cours.items(), key=lambda p: (p[0][0], p[0][1], sans_accents(p[0][2]))):
                    print(f"- {cle[2]} : {valeur} {accord(valeur, 'série', 'séries')}")
                print()
                print(f"=== Fréquence d'entraînement ===\n")
                frequence_par_groupe, frequence_par_muscle = frequence_groupe_et_par_muscle_par_semaine(seances)
                frequence_par_groupe_semaine_en_cours = {cle: valeur for cle, valeur in frequence_par_groupe.items() if cle[0] == annee and cle[1] == num_semaine}
                frequence_par_muscle_semaine_en_cours = {cle: valeur for cle, valeur in frequence_par_muscle.items() if cle[0] == annee and cle[1] == num_semaine}
                print(f"--- Fréquence par groupe ---\n")
                for cle, valeur in sorted(frequence_par_groupe_semaine_en_cours.items(), key=lambda p: (p[0][0], p[0][1], sans_accents(p[0][2]))):
                    print(f"-{cle[2]} : {valeur} fois")
                print()
                print(f"--- Fréquence par muscle ---\n")
                for cle, valeur in sorted(frequence_par_muscle_semaine_en_cours.items(), key=lambda p: (p[0][0], p[0][1], sans_accents(p[0][2]))):
                    print(f"- {cle[2]} : {valeur} fois")
                print()
                print(f"=== Comparaison aux fourchettes scientifiques ===\n")
                comparaison_fourchette_scientifique = comparaison_nb_series_par_groupe_et_fourchette_scientifique(seances)
                comparaison_fourchette_scientifique_semaine_en_cours = {cle: valeur for cle, valeur in comparaison_fourchette_scientifique.items() if cle[0] == annee and cle[1] == num_semaine}
                for cle, donnees in sorted(comparaison_fourchette_scientifique_semaine_en_cours.items(), key=lambda p: (p[0][0], p[0][1], sans_accents(p[0][2]))):
                    print(f"- {cle[2]} : {donnees['nb_series']} {accord(donnees['nb_series'], 'série', 'séries')} | {donnees['statut']}")
                print()

            elif choix == "6":
                print(f"=== Evolution des charges dans le temps ===")
                seances = charger_toutes_les_seances_completes(session)
                resultat = evolution_des_charges_dans_le_temps(seances)
                if not resultat:
                    print(f"Aucun exercice enregistré")
                    continue
                for nom, liste in sorted(resultat.items(), key=lambda p: sans_accents(p[0])):
                    print(f"\n  {nom} :")
                    for date_seance, charge in liste:
                        print(f"    {date_seance} : {charge:.1f} kg")
            elif choix == "7":
                print(f"=== Exercices pratiqués par groupe ===")
                seances = charger_toutes_les_seances_completes(session)
                resultat = lister_exercices_differents_par_groupe(seances)
                if not resultat:
                    print("Aucun exercice enregistré")
                    continue
                for groupe, liste in sorted(resultat.items(), key=lambda p: sans_accents(p[0])):
                    print(f"\n  {groupe} :")
                    for nom in liste:
                        print(f"    -{nom}")
            elif choix == "8":
                print(f"=== Mes records ===\n")
                seances = charger_toutes_les_seances_completes(session)
                if not seances:
                    print("Aucune séance enregistrée")
                    continue
                afficher_records(session)
                print()
                print(f"=== Mes 1RM ===")
                for nom, rm in sorted(un_rm_estime_par_exercice(seances).items(), key=lambda p: sans_accents(p[0])):
                    print(f"\n  {nom} :")
                    print(f"    {rm:.1f} kg")
            elif choix == "9":
                supprimer_seances(session)
            elif choix == "10":
                modifier_seance(session)
            elif choix == "0":
                print("À bientôt !")
                logger.info("Fermeture de l'application")
                break
            else:
                print("Choix invalide")

if __name__ == "__main__":
    configurer_logging()
    lancer_application()

