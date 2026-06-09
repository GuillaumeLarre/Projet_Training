from Interface.Interface import (afficher_menu, saisir_seance, afficher_records, saisir_exercice, lister_catalogue)

from Models.CarnetEntrainement import CarnetEntrainement

def lancer_application():
    carnet = CarnetEntrainement.charger("carnet.json")
    while True:
        afficher_menu()
        choix = input("Entre ton choix : ")
        if choix == "1":
            saisir_seance(carnet)
            carnet.sauvegarder("carnet.json") 
        elif choix == "2":
            carnet.afficher_historique()
        elif choix == "3":
            afficher_records(carnet)
        elif choix == "4":
            saisir_exercice(carnet)
            carnet.sauvegarder("carnet.json") 
        elif choix == "5":
            lister_catalogue(carnet)
        elif choix == "0":
            carnet.sauvegarder("carnet.json") 
            print("À bientôt !")
            break
        else:
            print("Choix invalide")

if __name__ == "__main__":
    lancer_application()
