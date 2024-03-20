import sys
import bdd
from PyQt5.QtWidgets import * #PETITE RAPPEL : POUR UTILISER PyQT5 ON DOIT L'INSTALLER AVEC "pip install PyQT5"
from PyQt5.QtCore import *
from functools import partial #utilisé dans afficher_liste_contact pour garder le bon I pour chaque bouton
from PyQt5.QtGui import QPixmap, QPainter, QBitmap, QImageReader, QImage, QIcon #ajout pour pouvoir s'occuper des images

Width = 400 #on les considère comme des constantes - NE JAMAIS LES MODIFIER DANS LE CODE
Height = 550
# projet final

def ifNone(chaine_de_char):
    if chaine_de_char == "None" or chaine_de_char == "" or chaine_de_char == None:
        return ""
    return chaine_de_char

def ajouter_contact_bouton(content_layout):#action réalisé par le bouton d'ajout d'un contact qui permet d'ajouter le contact à la bdd
    prenom_input = None
    nom_input = None
    surnom_input = None
    photo_input = None
    entreprise_input = None
    adresses = []
    adressemail_input = []
    numeros_input = []

    for index in range(content_layout.count()): #on fait une boucle de la taille d'objet qu'il y a dans le content_layout qui contient toutes les entrées de texte
        widget = content_layout.itemAt(index).widget()#on prend le widget à l'index donné par la boucle 
        if isinstance(widget, QLineEdit): #si c'est un QlineEdit (donc une entrée de texte) on vérifie laquel c'est grace à son nom
            if widget.objectName() == "prenom":
                prenom_input = widget.text() if widget.text() != "" else None
            elif widget.objectName() == "nom":
                nom_input = widget.text() if widget.text() != "" else None
            elif widget.objectName() == "surnom":
                surnom_input = widget.text() if widget.text() != "" else None
            elif widget.objectName() == "entreprise":
                entreprise_input = widget.text() if widget.text() != "" else None
            elif widget.objectName() == "photo":
                photo_input = widget.text() if widget.text() != "" else None
            #pour les valeurs suivante on ne peut pas le mettre juste dans une variable car il peut y avoir plusieurs valeurs, on le met donc dans une liste pour pouvoir les prendre tous en compte ( si on mettais juste dans une variable alors on aurait juste la dernière valeur trouvé)
            elif widget.objectName() in ["codepostal", "ville", "pays", "nomrue", "nbrue"]:#si le widget est lié à une adresse alors on le met dans adresses pour le calcul apres
                adresses.append(widget.text())
            elif widget.objectName() == "adressemail":
                adressemail_input.append(widget.text())
            elif widget.objectName() == "numeros":
                numeros_input.append(widget.text())
    
    # on obtient le chemin de l'image depuis le champ de texte de l'image
    image_binaire = None
    if photo_input:
        with open(photo_input, 'rb') as file:
            image_binaire = file.read()

    idcontact = bdd.ajouter_contact_main(nom_input, prenom_input, surnom_input, image_binaire, entreprise_input) #on ajoute les infos de base du contact puis on recup l'id du contact pour ajouter les autres infos qui sont dans d'autres tables

    # on rempli les zone potentiellement vide qui n'ont pas été entrées
    while len(adresses) % 5 != 0 and len(adresses) > 1:
        adresses.append(None)
    for i in range(0, len(adresses), 5): #petite boucle qui prend dans adresses(qui contient toutes les infos les une apres les autres des adresse entrées) l'adresse de chacun qui fait 5 de long (un peu compliqué a expliquer je sais xD)
        if all(value is None or value == '' for value in adresses[i:i+5]): #si les 5 infos de l'adresse sont vide alors on le considère pas car vu que rien rentré dedans sa sert a rien de l'ajouter dans la bdd
            continue

        codepostal = adresses[i] if adresses[i] else None
        ville = adresses[i + 1] if adresses[i + 1] else None
        pays = adresses[i + 2] if adresses[i + 2] else None
        nomrue = adresses[i + 3] if adresses[i + 3] else None
        nbrue = adresses[i + 4] if adresses[i + 4] else None
        bdd.ajouter_contact_adresse(idcontact, codepostal, ville, pays, nomrue, nbrue)#on ajoute l'adresse qu'on a à l'index i dans le tableau adresses 

    for numero in numeros_input:
        if numero and numero.strip(): # on vérifie si le numéro n'est pas vide ou composé uniquement d'espaces
            bdd.ajouter_contact_numero(idcontact, numero)
    
    for email in adressemail_input:
        if email and email.strip(): # on vérifie si l'email n'est pas vide ou composé uniquement d'espaces
            bdd.ajouter_contact_mail(idcontact, email)
    
def fermeture_des_widgets(*args): #permet de fermer tous les widgets (NE MET PAS DE LAYOUT SA MARCHERA PAS)
    for arg in args: 
        arg.close()

def fermeture_widgets_menu_contact(scroll_zone_contacts,empty_zone,scroll_zone,bouton_rechercher,zt_contact,bouton_modifier,contact_widget):
    if(empty_zone):
        empty_zone.close()
    if(scroll_zone):
        scroll_zone.close()
    if(bouton_rechercher):
        bouton_rechercher.close()
    if(zt_contact):
        zt_contact.close()
    if(bouton_modifier):
        bouton_modifier.close()
    if(contact_widget):
        contact_widget.close()
    actualiser_liste_contacts(scroll_zone_contacts,None)
    
def fermeture_et_ajout_contact(scroll_zone_contacts,zone_sombre, empty_zone, scroll_zone, zt_nouveau_contact, bouton_annuler, bouton_ok,content_layout):#permet juste au bouton ajouter d'ensuite fermer le sous menu d'ajout pour un souci d'ergonomie
    ajouter_contact_bouton(content_layout)
    content_widget = QWidget()
    content_widget.setLayout(content_layout)
    fermeture_des_widgets(zone_sombre, empty_zone, scroll_zone, zt_nouveau_contact, bouton_annuler, bouton_ok,content_widget)
    actualiser_liste_contacts(scroll_zone_contacts,None)

def update_bouton_ok(bouton_ok, prenom_input, nom_input, surnom_input, entreprise_input):#vérifie si des champs principaux est remplie pendant l'ajout d'un contact : si oui alors le bouton OK fonctionne sinon bah il fonctionne pas lol 
    if prenom_input.text() or nom_input.text() or surnom_input.text() or entreprise_input.text():
        bouton_ok.setEnabled(True)
    else:
        bouton_ok.setEnabled(False)

def update_zone_recherche(zone_rechercher,scroll_zone_contacts):#permet d'actualiser la liste des contacts affiché à l'écran sur le main_menu, si y'a rien d'écrit dedans alors on affiche tous
    if(zone_rechercher.text()==None):
        resultat = bdd.rechercher_contact(None)
    else:
        resultat = bdd.rechercher_contact(zone_rechercher.text())
    afficher_liste_contacts(scroll_zone_contacts,resultat)

def ajout_contact_menu(scroll_zone_contacts):#affiche le menu pour ajouter un contact
    zone_sombre = QWidget(fenetre)
    zone_sombre.setGeometry(0, 0, Width, Height)
    zone_sombre.setStyleSheet("background-color: rgba(0,0,0,100); ")
    zone_sombre.show()

    empty_zone = QWidget(fenetre)
    empty_zone.setGeometry(0, 50, Width, Height)
    empty_zone.setStyleSheet("background-color: rgb(0,0,0); border-radius: 14px;")
    empty_zone.show()

    scroll_zone = QScrollArea(fenetre)
    scroll_zone.setGeometry(0, 100, Width, Height - 100)
    scroll_zone.setWidgetResizable(True)
    scroll_zone.show()

    bouton_annuler = QPushButton('Annuler', fenetre)
    bouton_annuler.setGeometry(10, 60, 80, 25)
    bouton_annuler.clicked.connect(
        lambda: fermeture_des_widgets(zone_sombre, empty_zone, scroll_zone, bouton_annuler, bouton_ok, zt_nouveau_contact, content_widget))
    bouton_annuler.show()

    zt_nouveau_contact = QLabel('Nouveau Contact', fenetre)
    zt_nouveau_contact.setGeometry(int(Width / 2 - 70), 56, 140, 20)
    zt_nouveau_contact.show()

    content_widget = QWidget()
    content_layout = QVBoxLayout()
    content_layout.setAlignment(Qt.AlignTop)
    content_layout.setContentsMargins(0, 0, 0, 0)

    #ajout du bouton pour ajouter l'image (quel enfer c'était de l'importer sans bug avec le reste du code xD)
    photo_input = QLineEdit()
    bouton_selection_image = QPushButton('Sélectionner une image', fenetre)
    bouton_selection_image.setGeometry(10, 120, 150, 30)
    bouton_selection_image.clicked.connect(lambda: selectionner_image(content_layout,photo_input,None))
    content_layout.addWidget(bouton_selection_image)


    prenom_input = QLineEdit()
    prenom_input.setObjectName("prenom")
    prenom_input.setPlaceholderText('Prénom')
    prenom_input.textChanged.connect(
        lambda: update_bouton_ok(bouton_ok, prenom_input, nom_input, surnom_input, entreprise_input))
    content_layout.addWidget(prenom_input)

    nom_input = QLineEdit()
    nom_input.setObjectName("nom")
    nom_input.setPlaceholderText('Nom')
    nom_input.textChanged.connect(
        lambda: update_bouton_ok(bouton_ok, prenom_input, nom_input, surnom_input, entreprise_input))
    content_layout.addWidget(nom_input)

    surnom_input = QLineEdit()
    surnom_input.setObjectName("surnom")
    surnom_input.setPlaceholderText('Surnom')
    surnom_input.textChanged.connect(
        lambda: update_bouton_ok(bouton_ok, prenom_input, nom_input, surnom_input, entreprise_input))
    content_layout.addWidget(surnom_input)

    entreprise_input = QLineEdit()
    entreprise_input.setObjectName("entreprise")
    entreprise_input.setPlaceholderText('Entreprise')
    entreprise_input.textChanged.connect(
        lambda: update_bouton_ok(bouton_ok, prenom_input, nom_input, surnom_input, entreprise_input))
    content_layout.addWidget(entreprise_input)

   
    bouton_ajouter_une_adresse = QPushButton('Ajouter une adresse',fenetre)
    bouton_ajouter_une_adresse.clicked.connect(lambda: ajouter_champ_adresse(content_layout,bouton_ajouter_une_adresse))
    content_layout.addWidget(bouton_ajouter_une_adresse)

    bouton_ajouter_un_email = QPushButton('Ajouter un Email', fenetre)
    bouton_ajouter_un_email.clicked.connect(lambda: ajouter_champ_mail(content_layout,bouton_ajouter_un_email))
    content_layout.addWidget(bouton_ajouter_un_email)

    # Bouton "ajouter un numero" pour ajouter un nouveau champ de numéro
    bouton_ajouter_un_numero = QPushButton('Ajouter un numéro', fenetre)
    bouton_ajouter_un_numero.clicked.connect(lambda: ajouter_champ_numero(content_layout,bouton_ajouter_un_numero))
    content_layout.addWidget(bouton_ajouter_un_numero)

    content_widget.setLayout(content_layout)
    scroll_zone.setWidget(content_widget)

    # On crée d'abord le bouton OK avec l'option enabled à False
    bouton_ok = QPushButton('OK', fenetre)
    bouton_ok.setGeometry(Width - 40, 60, 30, 25)
    bouton_ok.setEnabled(False)
    #bouton_ok.clicked.connect(lambda: fermeture_et_ajout_contact(zone_sombre, empty_zone, scroll_zone, zt_nouveau_contact, bouton_annuler, bouton_ok, prenom_input, nom_input,entreprise_input, surnom_input, codepostal_input, ville_input, pays_input, nomrue_input, nbrue_input, adressemail_input))
    bouton_ok.clicked.connect(lambda: fermeture_et_ajout_contact(scroll_zone_contacts,zone_sombre, empty_zone, scroll_zone, zt_nouveau_contact, bouton_annuler, bouton_ok,content_layout))
    
    bouton_ok.show()

def selectionner_image(content_layout, photo_input,ancienne_image):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fichier, _ = QFileDialog.getOpenFileName(fenetre, "Sélectionner une image", "", "Images (*.png *.jpg *.bmp *.jpeg *.gif *.tiff *.tif);;Tous les fichiers (*)", options=options)
    
    for index in range(content_layout.count()): #on fait une boucle de la taille d'objet qu'il y a dans le content_layout qui contient toutes les entrées de texte
        widget = content_layout.itemAt(index).widget()#on prend le widget à l'index donné par la boucle 
        if isinstance(widget, QLabel) and widget.objectName() =="Image":
            widget.close()
            
    if fichier:
        if ancienne_image:
            ancienne_image.hide()
        photo_input.setText(fichier)
        afficher_image_cercle(content_layout, fichier)
        photo_input.setObjectName("photo")
        content_layout.addWidget(photo_input)
        photo_input.hide()#permet de cacher l'emplacement de la photo

def afficher_image_cercle(content_layout, image_path):
    # Charger l'image
    image = QPixmap(image_path)

    # Créer une image masque pour rendre l'image circulaire
    mask = QBitmap(image.size())
    mask.fill(Qt.white)

    painter = QPainter(mask)
    painter.setBrush(Qt.black)
    painter.drawEllipse(0, 0, image.width(), image.height())
    painter.end()

    image.setMask(mask)

    # Créer un QLabel pour afficher l'image
    label = QLabel()
    label.setPixmap(image.scaled(100, 100, Qt.KeepAspectRatio))  # Ajuste la taille selon les dimensions données avec 100 et 100
    label.setObjectName("Image")
    # Ajouter le QLabel contenant l'image au content_layout
    index = 0 #utilisé pour afficher l'image au bon endroit (flemme d'aller le chercher en utilisant la variable d'index du bouton donc je met directement le nombre car normalemnt il change pas de place)
    content_layout.addWidget(label)
    content_layout.insertWidget(index, label)

def ajouter_champ_adresse(content_layout,bouton_ajouter_une_adresse):#génère 5 nouveaux champs pour l'adresses : codepostal, ville, pays, nom de la rue et enfin le numero de la rue
    index_bouton_adresse = content_layout.indexOf(bouton_ajouter_une_adresse)
    zt_adresse = QLabel("Ajouter une adresse",fenetre)
    content_layout.insertWidget(index_bouton_adresse + 1,zt_adresse)

    codepostal_input = QLineEdit()
    codepostal_input.setObjectName("codepostal")
    codepostal_input.setPlaceholderText('Code Postal')
    content_layout.addWidget(codepostal_input)

    ville_input = QLineEdit()
    ville_input.setObjectName("ville")
    ville_input.setPlaceholderText('Ville')
    content_layout.addWidget(ville_input)

    pays_input = QLineEdit()
    pays_input.setObjectName("pays")
    pays_input.setPlaceholderText('Pays')
    content_layout.addWidget(pays_input)

    nomrue_input = QLineEdit()
    nomrue_input.setObjectName("nomrue")
    nomrue_input.setPlaceholderText('Nom de rue')
    content_layout.addWidget(nomrue_input)

    nbrue_input = QLineEdit()
    nbrue_input.setObjectName("nbrue")
    nbrue_input.setPlaceholderText('Numéro de rue')
    content_layout.addWidget(nbrue_input)

    
    content_layout.insertWidget(index_bouton_adresse + 2, codepostal_input)
    content_layout.insertWidget(index_bouton_adresse + 3, ville_input)
    content_layout.insertWidget(index_bouton_adresse + 4, pays_input)
    content_layout.insertWidget(index_bouton_adresse + 5, nomrue_input)
    content_layout.insertWidget(index_bouton_adresse + 6, nbrue_input)

def ajouter_champ_numero(content_layout,bouton_ajouter_un_numero):#génère un nouveau champ pour le numéro
    nouveaux_numeros_input = QLineEdit()
    nouveaux_numeros_input.setObjectName("numeros")
    nouveaux_numeros_input.setPlaceholderText('Numéros')

    index_bouton_numero = content_layout.indexOf(bouton_ajouter_un_numero)
    content_layout.insertWidget(index_bouton_numero + 1, nouveaux_numeros_input)

def ajouter_champ_mail(content_layout,bouton_ajouter_un_email):#génère un nouveau champ pour le mail
    nouveaux_mail_input = QLineEdit()
    nouveaux_mail_input.setObjectName("adressemail")
    nouveaux_mail_input.setPlaceholderText('Email')

    index_bouton_mail = content_layout.indexOf(bouton_ajouter_un_email)
    content_layout.insertWidget(index_bouton_mail + 1, nouveaux_mail_input)

def suppression_contact(scroll_zone_contacts,idcontact,zone_sombre, empty_zone, scroll_zone, bouton_annuler, bouton_valider, zt_nouveau_contact, content_widget, empty_zone_menu, scroll_zone_menu, bouton_rechercher, zt_contact, bouton_modifier, contact_widget_menu):
    bdd.supprimer_contact_adresse(idcontact,None)
    bdd.supprimer_contact_numero(idcontact,None)
    bdd.supprimer_contact_mail(idcontact,None)
    bdd.supprimer_contact_main(idcontact)
    fermeture_des_widgets(zone_sombre, empty_zone, scroll_zone, bouton_annuler, bouton_valider, zt_nouveau_contact, content_widget,empty_zone_menu,scroll_zone_menu,bouton_rechercher,zt_contact,bouton_modifier,contact_widget_menu)
    actualiser_liste_contacts(scroll_zone_contacts,None)

def modifier_contact(scroll_zone_contacts,idcontact,contact,adresses,numeros,emails,scroll_zone_menu,empty_zone_menu,bouton_rechercher,zt_contact,bouton_modifier,contact_widget):#permet de modifier un contact
    print("Menu de modification")
    zone_sombre = QWidget(fenetre)
    zone_sombre.setGeometry(0, 0, Width, Height)
    zone_sombre.setStyleSheet("background-color: rgba(0,0,0,100); ")
    zone_sombre.show()

    empty_zone = QWidget(fenetre)
    empty_zone.setGeometry(0, 50, Width, Height)
    empty_zone.setStyleSheet("background-color: rgb(0,0,0); border-radius: 10px;")
    empty_zone.show()

    scroll_zone = QScrollArea(fenetre)
    scroll_zone.setGeometry(0, 100, Width, Height - 100)
    scroll_zone.setWidgetResizable(True)
    scroll_zone.show()

    bouton_annuler = QPushButton('Annuler', fenetre)
    bouton_annuler.setGeometry(10, 60, 80, 25)
    bouton_annuler.clicked.connect(
        lambda: fermeture_des_widgets(zone_sombre, empty_zone, scroll_zone, bouton_annuler, bouton_valider, zt_nouveau_contact, content_widget))
    bouton_annuler.show()

    zt_nouveau_contact = QLabel('Modifier Contact', fenetre)
    zt_nouveau_contact.setGeometry(int(Width / 2 - 50), 56, 100, 20)
    zt_nouveau_contact.show()

    content_widget = QWidget()
    content_layout = QVBoxLayout()
    content_layout.setAlignment(Qt.AlignTop)
    content_layout.setContentsMargins(0, 0, 0, 0)

    labelImage = QLabel()
    affichage_image_depuis_bdd(idcontact,labelImage)
    content_layout.addWidget(labelImage)
    #ajout du bouton pour ajouter l'image (quel enfer c'était de l'importer sans bug avec le reste du code xD)
    photo_input = QLineEdit()
    photo_input.setText(None) #on le met à None ( comme sa si une nouvelle image est loadé il sera plus a None)
    bouton_selection_image = QPushButton('Sélectionner une nouvelle image', fenetre)
    bouton_selection_image.setGeometry(10, 120, 150, 30)
    bouton_selection_image.clicked.connect(lambda: selectionner_image(content_layout,photo_input,labelImage))
    content_layout.addWidget(bouton_selection_image)

    prenom_input = QLineEdit()
    prenom_input.setObjectName("prenom")
    prenom_input.setPlaceholderText('Prénom')
    prenom_input.setText(ifNone(str(contact[0][2])))
    prenom_input.textChanged.connect(
        lambda: update_bouton_ok(bouton_valider, prenom_input, nom_input, surnom_input, entreprise_input))#on peut réutiliser update_bouton_ok car on fait la meme vérification
    content_layout.addWidget(prenom_input)

    nom_input = QLineEdit()
    nom_input.setObjectName("nom")
    nom_input.setPlaceholderText('Nom')
    nom_input.setText(ifNone(str(contact[0][1])))
    nom_input.textChanged.connect(
        lambda: update_bouton_ok(bouton_valider, prenom_input, nom_input, surnom_input, entreprise_input))#on peut réutiliser update_bouton_ok car on fait la meme vérification
    content_layout.addWidget(nom_input)

    surnom_input = QLineEdit()
    surnom_input.setObjectName("surnom")
    surnom_input.setPlaceholderText('Surnom')
    surnom_input.setText(ifNone(str(contact[0][3])))
    surnom_input.textChanged.connect(
        lambda: update_bouton_ok(bouton_valider, prenom_input, nom_input, surnom_input, entreprise_input))#on peut réutiliser update_bouton_ok car on fait la meme vérification
    content_layout.addWidget(surnom_input)

    entreprise_input = QLineEdit()
    entreprise_input.setObjectName("entreprise")
    entreprise_input.setPlaceholderText('Entreprise')
    entreprise_input.setText(ifNone(str(contact[0][4])))
    entreprise_input.textChanged.connect(
        lambda: update_bouton_ok(bouton_valider, prenom_input, nom_input, surnom_input, entreprise_input))#on peut réutiliser update_bouton_ok car on fait la meme vérification
    content_layout.addWidget(entreprise_input)

   
    
    #affichage des adresses
    zt_adresses = QLabel("Liste des adresses",fenetre)
    content_layout.addWidget(zt_adresses)

    bouton_ajouter_une_adresse = QPushButton('Ajouter une adresse',fenetre)
    bouton_ajouter_une_adresse.clicked.connect(lambda: ajouter_champ_adresse(content_layout,bouton_ajouter_une_adresse))
    content_layout.addWidget(bouton_ajouter_une_adresse)
    for i in range(len(adresses)):
        zt_adresse = QLabel("Adresse n°"+ str(i+1) +" : ",fenetre)
        content_layout.addWidget(zt_adresse)


        ida = QLineEdit() #utilisé pour avoir l'id de l'adresse pour ensuite la modifier au lieu d'en recréer une
        ida.setText(str(adresses[i][0]))
        ida.setObjectName("ida")
        ida.hide()
        content_layout.addWidget(ida)

        codepostal = QLineEdit()
        codepostal.setObjectName("oldCodePostal")
        codepostal.setText(ifNone(str(adresses[i][2])))
        codepostal.setPlaceholderText("Code Postal")
        content_layout.addWidget(codepostal)

        ville = QLineEdit()
        ville.setObjectName("oldVille")
        ville.setText(ifNone(str(adresses[i][3])))
        ville.setPlaceholderText("Ville")
        content_layout.addWidget(ville)

        pays = QLineEdit()
        pays.setObjectName("oldPays")
        pays.setText(ifNone(str(adresses[i][4])))
        pays.setPlaceholderText("Pays")
        content_layout.addWidget(pays)

        nomrue = QLineEdit()
        nomrue.setObjectName("oldNomrue")
        nomrue.setText(ifNone(str(adresses[i][5])))
        nomrue.setPlaceholderText("Nom de Rue")
        content_layout.addWidget(nomrue)

        nbrue = QLineEdit()
        nbrue.setObjectName("oldNbrue")
        nbrue.setText(ifNone(str(adresses[i][6])))
        nbrue.setPlaceholderText("Numéro de Rue")
        content_layout.addWidget(nbrue)
    

    #afficahge des numéros
    zt_numeros = QLabel("Liste des numéros",fenetre)
    content_layout.addWidget(zt_numeros)
    # Bouton "ajouter un numero" pour ajouter un nouveau champ de numéro
    bouton_ajouter_un_numero = QPushButton('Ajouter un numéro', fenetre)
    bouton_ajouter_un_numero.clicked.connect(lambda: ajouter_champ_numero(content_layout,bouton_ajouter_un_numero))
    content_layout.addWidget(bouton_ajouter_un_numero)
    for j in range(len(numeros)):
        idn = QLineEdit()#permet de recup l'id du numero de tel
        idn.setText(str(numeros[j][0]))
        idn.setObjectName("idn")
        idn.hide()
        content_layout.addWidget(idn)

        numero = QLineEdit()
        numero.setObjectName("oldNumero")
        numero.setText(ifNone(str(numeros[j][2])))
        content_layout.addWidget(numero)
    
    #affichage des mails
    zt_emails = QLabel("Liste des Emails",fenetre)
    content_layout.addWidget(zt_emails)
    #bouton ajouter un Email
    bouton_ajouter_un_email = QPushButton('Ajouter un Email', fenetre)
    bouton_ajouter_un_email.clicked.connect(lambda: ajouter_champ_mail(content_layout,bouton_ajouter_un_email))
    content_layout.addWidget(bouton_ajouter_un_email)
    for k in range(len(emails)):
        ide = QLineEdit()#permet de recup l'id du mail
        ide.setText(str(emails[k][0]))
        ide.setObjectName("ide")
        ide.hide()
        content_layout.addWidget(ide)

        mail = QLineEdit()
        mail.setObjectName("oldMail")
        mail.setText(ifNone(str(emails[k][2])))
        content_layout.addWidget(mail)

    bouton_supprimer = QPushButton('Supprimer le contact',fenetre)
    #lambda: fermeture_widgets(zone_sombre, empty_zone, scroll_zone, bouton_annuler, bouton_valider, zt_nouveau_contact, content_layout))
    bouton_supprimer.clicked.connect(lambda: suppression_contact(scroll_zone_contacts, idcontact, zone_sombre, empty_zone, scroll_zone, bouton_annuler, bouton_valider, zt_nouveau_contact, content_widget,scroll_zone_menu,empty_zone_menu,bouton_rechercher,zt_contact,bouton_modifier,contact_widget))
    content_layout.addWidget(bouton_supprimer)

    content_widget.setLayout(content_layout)
    scroll_zone.setWidget(content_widget)

    # On crée d'abord le bouton OK avec l'option enabled à False
    bouton_valider = QPushButton('Valider', fenetre)
    bouton_valider.setGeometry(Width - 80, 60, 70, 25)
    bouton_valider.clicked.connect(lambda: fermeture_et_modification_contact(zone_sombre, empty_zone, scroll_zone, bouton_annuler, bouton_valider, zt_nouveau_contact, content_widget,idcontact,photo_input))
    bouton_valider.show()

def bouton_modification(idcontact,content_widget,photo_input_old):

    content_layout = content_widget.layout()
    prenom_input = None
    nom_input = None
    photo_input = None
    surnom_input = None
    entreprise_input = None
    adresses = []
    adressemail_input = []
    numeros_input = []
    oldAdresses = []
    oldAdressemail_input = []
    oldNumeros_input = []

    for index in range(content_layout.count()): #on fait une boucle de la taille d'objet qu'il y a dans le content_layout qui contient toutes les entrées de texte
        widget = content_layout.itemAt(index).widget()#on prend le widget à l'index donné par la boucle 
        if isinstance(widget, QLineEdit): #si c'est un QlineEdit (donc une entrée de texte) on vérifie laquel c'est grace à son nom
            if widget.objectName() == "prenom":
                prenom_input = widget.text() if widget.text() != "" or widget.text() != "None" else None
            elif widget.objectName() == "nom":
                nom_input = widget.text() if widget.text() != "" or widget.text() != "None" else None
            elif widget.objectName() == "surnom":
                surnom_input = widget.text() if widget.text() != "" or widget.text() != "None" else None
            elif widget.objectName() == "entreprise":
                entreprise_input = widget.text() if widget.text() != "" or widget.text() != "None" else None
            elif widget.objectName() == "photo":
                photo_input = widget.text() if widget.text() != "" or widget.text() != "None" else None
            #on est obligé de séparer les nouveaux champs des anciens
            elif widget.objectName() in ["ida","oldCodePostal", "oldVille", "oldPays", "oldNomrue", "oldNbrue"]:#si le widget est lié à une adresse alors on le met dans adresses pour le calcul apres
                oldAdresses.append(widget.text())
            elif widget.objectName() in ["ide","oldMail"]:
                oldAdressemail_input.append(widget.text())
            elif widget.objectName() in ["idn","oldNumero"]:
                oldNumeros_input.append(widget.text())
            #les nouveaux champs qu'on va créer
            elif widget.objectName() in ["codepostal", "ville", "pays", "nomrue", "nbrue"]:#si le widget est lié à une adresse alors on le met dans adresses pour le calcul apres
                adresses.append(widget.text())
            elif widget.objectName() == "adressemail":
                adressemail_input.append(widget.text())
            elif widget.objectName() =="numeros":
                numeros_input.append(widget.text())
    
    # on obtient le chemin de l'image depuis le champ de texte de l'image
    if(photo_input_old):
        photo = bdd.select_photo(idcontact)
        print(photo[0][0])
        bdd.modifier_contact_main(idcontact,nom_input,prenom_input,surnom_input,photo[0][0],entreprise_input)
    else:
        image_binaire = None
        if photo_input:
            with open(photo_input, 'rb') as file:
                image_binaire = file.read()
        bdd.modifier_contact_main(idcontact,nom_input,prenom_input,surnom_input,image_binaire,entreprise_input)

    while len(oldAdresses) % 6 != 0 and len(oldAdresses) > 1:
        oldAdresses.append(None)
    for i in range(0, len(oldAdresses), 6): 
        if all(value is None or value == '' for value in oldAdresses[i+1:i+6]): 
            bdd.supprimer_contact_adresse(None,oldAdresses[i])
            continue
        ida = oldAdresses[i]
        codepostal = oldAdresses[i+1] if oldAdresses[i+1] else None
        ville = oldAdresses[i + 2] if oldAdresses[i + 2] else None
        pays = oldAdresses[i + 3] if oldAdresses[i + 3] else None
        nomrue = oldAdresses[i + 4] if oldAdresses[i + 4] else None
        nbrue = oldAdresses[i + 5] if oldAdresses[i + 5] else None
        bdd.modifier_contact_adresse(ida, codepostal, ville, pays, nomrue, nbrue)

    for i in range(0,len(oldNumeros_input),2):
        if oldNumeros_input[i+1] is None or oldNumeros_input[i+1] == '' or oldNumeros_input[i+1] == "None" :
            bdd.supprimer_contact_numero(None,oldNumeros_input[i])
            continue
        idn = oldNumeros_input[i] if oldNumeros_input[i] else None
        numero = oldNumeros_input[i + 1] if oldNumeros_input[i + 1] else None
        bdd.modifier_contact_numero(idn,numero)
    
    for i in range(0,len(oldAdressemail_input),2):
        if oldAdressemail_input[i+1] is None or oldAdressemail_input[i+1] == '' or oldAdressemail_input[i+1] == "None":
            bdd.supprimer_contact_mail(None,oldAdressemail_input[i])
            continue
        idm = oldAdressemail_input[i] if oldAdressemail_input[i] else None
        mail = oldAdressemail_input[i + 1] if oldAdressemail_input[i + 1] else None
        bdd.modifier_contact_mail(idm,mail)

    #------------------------------------- pareil que dans ajouter_contact_bouton ----------------------------------------------------
    # on rempli les zone potentiellement vide qui n'ont pas été entrées
    while len(adresses) % 5 != 0 and len(adresses) > 1:
        adresses.append(None)
    for i in range(0, len(adresses), 5): #petite boucle qui prend dans adresses(qui contient toutes les infos les une apres les autres des adresse entrées) l'adresse de chacun qui fait 5 de long (un peu compliqué a expliquer je sais xD)
        if all(value is None or value == '' for value in adresses[i:i+5]): #si les 5 infos de l'adresse sont vide alors on le considère pas car vu que rien rentré dedans sa sert a rien de l'ajouter dans la bdd
            continue
        codepostal = adresses[i] if adresses[i] else None
        ville = adresses[i + 1] if adresses[i + 1] else None
        pays = adresses[i + 2] if adresses[i + 2] else None
        nomrue = adresses[i + 3] if adresses[i + 3] else None
        nbrue = adresses[i + 4] if adresses[i + 4] else None
        bdd.ajouter_contact_adresse(idcontact, codepostal, ville, pays, nomrue, nbrue)#on ajoute l'adresse qu'on a à l'index i dans le tableau adresses 

    for numero in numeros_input:
        if numero and numero.strip(): # on vérifie si le numéro n'est pas vide ou composé uniquement d'espaces
            bdd.ajouter_contact_numero(idcontact, numero)
    
    for email in adressemail_input:
        if email and email.strip(): # on vérifie si l'email n'est pas vide ou composé uniquement d'espaces
            bdd.ajouter_contact_mail(idcontact, email)

def fermeture_et_modification_contact(zone_sombre, empty_zone, scroll_zone, bouton_annuler, bouton_valider, zt_nouveau_contact, content_widget, idcontact,photo_input):
    bouton_modification(idcontact,content_widget,photo_input)
    fermeture_des_widgets(zone_sombre, empty_zone, scroll_zone, bouton_annuler, bouton_valider, zt_nouveau_contact, content_widget)

def affichage_image_depuis_bdd(idcontact, label_widget):
    conn, cursor = bdd.connect_database()
    cursor.execute('''SELECT photo FROM contacts WHERE idcontact=? ''',(idcontact,))
    image = cursor.fetchone()
    if image is not None:
        image_blob = image[0]
        pixmap = QPixmap()
        pixmap.loadFromData(image_blob)
        pixmap_resized = pixmap.scaled(100, 100, Qt.KeepAspectRatio)

        # Créer un masque rond pour le widget
        mask = QBitmap(pixmap_resized.size())
        mask.fill(Qt.white)
        painter = QPainter(mask)
        painter.setBrush(Qt.black)
        painter.drawEllipse(0, 0, 100, 100)
        painter.end()

        pixmap_resized.setMask(mask)

        label_widget.setPixmap(pixmap_resized)
        label_widget.setFixedSize(100, 100)
        
def afficher_contact_menu(idcontact,scroll_zone_contacts):#affiche un menu quand on clique sur le contact souhaité
    #partie loading des données du contact
    contact,adresses,numeros,emails= bdd.load_contact(idcontact)
    nom = contact[0][1]
    prenom = contact[0][2]
    surnom = contact[0][3]
    entreprise = contact[0][4]

    

    #zone pour afficher l'ensemble de la fiche contact
    empty_zone = QWidget(fenetre)
    empty_zone.setGeometry(0, 0, Width, Height) 
    empty_zone.setStyleSheet("background-color: rgb(0,0,0); border-radius: 10px;")
    # Style pour la fenêtre principale
    style_main_window = (
        "background-color: #2C2C2C;"  # Fond bleu foncé
    )
    fenetre.setStyleSheet(style_main_window)
    style_white_frame = (
        "border-radius: 10px;"  # Coins arrondis
        "padding: 10px;"  # Remplissage intérieur
    )

    empty_zone.setStyleSheet(style_white_frame)
    empty_zone.show()

    #bouton pour retourner au menu de recherche(BIEN PENSER A AJOUTER DEDANS TOUS LES WIDGETS DU MENU)
    bouton_rechercher = QPushButton('< Rechercher', fenetre)
    bouton_rechercher.setGeometry(10,10,100,25)
    bouton_rechercher.clicked.connect(lambda: fermeture_widgets_menu_contact(scroll_zone_contacts,empty_zone, scroll_zone, bouton_rechercher, zt_contact, bouton_modifier, contact_widget))
    bouton_rechercher.setStyleSheet(
        "background-color: #3498db; color: white; border: none; padding: 5px 10px; border-radius: 5px;")
    bouton_rechercher.show()
    
    t_contact = None
    #création de la string qui va s'afficher en haut de la fenetre pour dire sur quel contact on se trouve
    if(prenom!=None and nom!=None):
        t_contact = str(prenom) + " " + str(nom)#on affiche nom et prénom car ils sont présents
    elif(prenom!=None):
        t_contact = str(prenom)#affichage seulement du prénom car nom manquant
    elif(nom!=None):
        t_contact = str(nom)#affichage du surnom car nom et prénom manquant
    elif(surnom!=None):
        t_contact = str(surnom)#affichage du surnom car prénom et nom manquant
    elif(entreprise!=None):
        t_contact = str(entreprise)#affichage du nom de l'entreprise car tout les rest est manquant
    
    zt_contact = QLabel(t_contact, fenetre)
    zt_contact.setGeometry(150, 14, 300, 20)# A REGLER CAR LA POSISTION AU MILIEU DE L ECRAN NE FONCTIONNE PAS BIEN
    zt_contact.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C2C2C;")
    zt_contact.show()
    
    bouton_modifier = QPushButton('Modifier', fenetre)
    bouton_modifier.setGeometry(310,10,80,25)
    bouton_modifier.clicked.connect(lambda: modifier_contact(scroll_zone_contacts,idcontact,contact,adresses,numeros,emails,scroll_zone,empty_zone,bouton_rechercher,zt_contact,bouton_modifier,contact_widget))
    bouton_modifier.setStyleSheet(
        "background-color: #2ecc71; color: white; border: none; padding: 5px 10px; border-radius: 5px;")
    bouton_modifier.show()

    scroll_zone = QScrollArea(fenetre)
    scroll_zone.setGeometry(0, 40, Width, Height - 50)
    scroll_zone.setWidgetResizable(True)
    scroll_zone.show()

    contact_widget = QWidget()
    contact_layout = QVBoxLayout() #pour stocker les infos du contact
    contact_layout.setAlignment(Qt.AlignTop)
    contact_layout.setContentsMargins(20,20,20,20)
    #affichage de l'image (on fait comme on peut xD )
    labelImage = QLabel()
    affichage_image_depuis_bdd(idcontact,labelImage)
    contact_layout.addWidget(labelImage)
    # affichage des infos de base
    style_info_label = (

        ""
    )
    #affichage des infos de base
    zt_prenom = QLabel("Prénom : "+ifNone(str(prenom)),fenetre)
    zt_prenom.setStyleSheet(style_info_label)
    contact_layout.addWidget(zt_prenom)
    zt_nom = QLabel("Nom : "+ifNone(str(nom)),fenetre)
    zt_nom.setStyleSheet(style_info_label)
    contact_layout.addWidget(zt_nom)
    zt_surnom = QLabel("Surnom : "+ifNone(str(surnom)),fenetre)
    zt_surnom.setStyleSheet(style_info_label)
    contact_layout.addWidget(zt_surnom)
    zt_entreprise = QLabel("Entreprise : "+ifNone(str(entreprise)),fenetre)
    zt_entreprise.setStyleSheet(style_info_label)
    contact_layout.addWidget(zt_entreprise)

    #affichage des adresses
    zt_adresses = QLabel("Liste des adresses",fenetre)
    zt_adresses.setStyleSheet(style_info_label)
    contact_layout.addWidget(zt_adresses)
    for i in range(len(adresses)):
        zt_adresse = QLabel("Adresse n°"+ str(i+1) +" : ",fenetre)
        zt_adresse.setStyleSheet(style_info_label)
        contact_layout.addWidget(zt_adresse)
        zt_codepostal = QLabel("      Code Postal : "+ifNone(str(adresses[i][2])),fenetre)
        zt_codepostal.setStyleSheet(style_info_label)
        contact_layout.addWidget(zt_codepostal)
        zt_ville = QLabel("     Ville : "+ifNone(str(adresses[i][3])),fenetre)
        zt_ville.setStyleSheet(style_info_label)
        contact_layout.addWidget(zt_ville)
        zt_pays = QLabel("      Pays : "+ifNone(str(adresses[i][4])),fenetre)
        zt_pays.setStyleSheet(style_info_label)
        contact_layout.addWidget(zt_pays)
        zt_rue = QLabel("       Rue : "+ifNone(str(adresses[i][6])) +" "+ ifNone(str(adresses[i][5])),fenetre)
        zt_rue.setStyleSheet(style_info_label)
        contact_layout.addWidget(zt_rue)
    
    #afficahge des numéros
    zt_numeros = QLabel("Liste des numéros",fenetre)
    zt_numeros.setStyleSheet(style_info_label)
    contact_layout.addWidget(zt_numeros)
    for j in range(len(numeros)):
        zt_numero = QLabel("        Téléphone Numéro n°"+ str(j+1) +" : "+ifNone(str(numeros[j][2])),fenetre)
        zt_numero.setStyleSheet(style_info_label)
        contact_layout.addWidget(zt_numero)
    #affichage des mails
    zt_emails = QLabel("Liste des Emails",fenetre)
    zt_emails.setStyleSheet(style_info_label)
    contact_layout.addWidget(zt_emails)
    for k in range(len(emails)):
        zt_mail = QLabel("      Email n°"+ str(k+1) +" : "+ifNone(str(emails[k][2])),fenetre)
        zt_mail.setStyleSheet(style_info_label)
        contact_layout.addWidget(zt_mail)

    contact_widget.setLayout(contact_layout)
    scroll_zone.setWidget(contact_widget)

def afficher_liste_contacts(scroll_zone_contacts,resultat):#affiche la liste de contact
    #création du widget et du layout
    content_widget = QWidget()#creation du widget contenant l'ensemble des contacts
    content_layout = QVBoxLayout()#creation d'un layout pour placer verticalement la liste des contacts
    content_layout.setAlignment(Qt.AlignTop)#on l'aligne en haut pour éviter un affichage dégueu
    content_layout.setContentsMargins(0,0,0,0)#on retire les marges
    for i in range(len(resultat)):#boucle pour savoir ce que l'on va afficher pour le contact
        if(resultat[i][2]!=None and resultat[i][1]!=None):
            nomprenom = ifNone(str(resultat[i][2])) + " " + ifNone(str(resultat[i][1]))#on affiche nom et prénom car ils sont présents
        elif(resultat[i][2]!=None):
            nomprenom = ifNone(str(resultat[i][2]))#affichage seulement du prénom car nom manquant
        elif(resultat[i][1]!=None):
            nomprenom = ifNone(str(resultat[i][1]))#affichage du surnom car nom et prénom manquant
        elif(resultat[i][3]!=None):
            nomprenom = ifNone(str(resultat[i][3]))#affichage du surnom car prénom et nom manquant
        elif(resultat[i][4]!=None):
            nomprenom = ifNone(str(resultat[i][4]))#affichage du nom de l'entreprise car tout les rest est manquant
        else:
            continue #on continue au cas où le compte n'a aucune valeur (compte bugué (ne devrait jamais arriver))
        bouton_contact = QPushButton(nomprenom, fenetre)#on utilise des QPushButton car on veut pouvoir cliquer sur les contacts pour les voir en entier/ les modifier/les supprimer
        bouton_contact.setGeometry(360,6,30,30)
        bouton_contact.clicked.connect(partial(afficher_contact_menu,resultat[i][0],scroll_zone_contacts))
        bouton_contact.setStyleSheet(
            "QPushButton { background-color: #ddd; color: #333; font-size: 14px; border: none; border-radius: 5px; padding: 5px; margin: 5px; }"
            "QPushButton:hover { background-color: #ccc; }"
        )
        #afin de récupérer le bon id et non le dernier de la boucle on passe par la fonction partial qui permet de créer un fonction partielle qui permet de capturer la valeur de i au moment où la fonction est appelée (en gros on créer une fonction partielle qui stocke la valeur de i pour le bouton et qui ensuite va utiliser ce i et non la valeur de i au moment où le bouton est appuyé (qui est égal au dernier idcontact))
        content_layout.addWidget(bouton_contact)

    content_widget.setLayout(content_layout)#on set le layout de content_widget avec content layout qui possédait précédement les contacts (on fait comme cela car si on utilise pas de layout alors les boutons ne seront pas bien placé, en plus la zone de scroll doit prendre un widget et non un layout)
    scroll_zone_contacts.setWidget(content_widget)#on ajoute l'ensemble des contacts qui sont dans vbox dans scroll_zone

def actualiser_liste_contacts(scroll_zone_contacts,recherche):#permet d'acutaliser la liste des contacts affiché sur le main_menu
    recherche = bdd.rechercher_contact(recherche)
    afficher_liste_contacts(scroll_zone_contacts,recherche)

def main_menu(fenetre):#menu principal, normalement ne doit jamais être relancé
    

    background = QWidget(fenetre)
    background.setGeometry(0, 0, Width, Height)
    background.setStyleSheet("background-color: #2C2C2C; border-radius: 14px;")
    background.show()

    zt_contacts = QLabel('Contacts', fenetre)
    zt_contacts.setAlignment(Qt.AlignCenter)
    zt_contacts.setGeometry(0, 8, Width, 20)  # Position y = 56, largeur = Width, hauteur = 20
    zt_contacts.show()

    #zone de recherche(il faudra modifier afficher_liste_contact pour prendre en parametre ce qui est entrée sauf si rien n'est marquée)
    zone_rechercher = QLineEdit(fenetre)
    zone_rechercher.setGeometry(10, 40, 380, 30) #pos x | pos y | size x | size y
    zone_rechercher.setPlaceholderText('Rechercher')
    zone_rechercher.textChanged.connect(lambda: update_zone_recherche(zone_rechercher,scroll_zone_contacts))
    zone_rechercher.setStyleSheet(
        "QLineEdit {"
        "   background-color: #ffffff;"  # Blanc
        "   border: 1px solid #ccc;"
        "   border-radius: 5px;"
        "   padding: 5px;"
        "   color: #333;"  # Couleur du texte
        "}"
        "QLineEdit:focus {"
        "   border: 2px solid #4CAF50;"  # Lorsqu'il est en focus
        "}"
    )

    #bouton pour ajouter un contact
    bouton_ajout_contact = QPushButton('+',fenetre)
    bouton_ajout_contact.setGeometry(360,6,30,30)
    bouton_ajout_contact.setIcon(QIcon('Assets/ajt.png'))
    bouton_ajout_contact.clicked.connect(lambda: ajout_contact_menu(scroll_zone_contacts))

    #bouton pour actualiser la liste des contacts (implémenté en cas modif de la bdd par un autre User que celui qui regarde acutellement)
    bouton_actualiser_contact = QPushButton('actualiser',fenetre)
    bouton_actualiser_contact.setGeometry(260,6,95,30)
    bouton_actualiser_contact.setIcon(QIcon('Assets/actualiser.png'))
    bouton_actualiser_contact.clicked.connect(lambda: actualiser_liste_contacts(scroll_zone_contacts,zone_rechercher.text()))
    # Appliquer un style personnalisé à la zone de recherche
    zone_rechercher.setStyleSheet(
        "QLineEdit {  border: 1px solid #ccc; border-radius: 5px; }"
    )

    # Appliquer un style personnalisé au bouton d'ajout de contact
    bouton_ajout_contact.setStyleSheet(
        "QPushButton { background-color: #4CAF50; color: white; font-size: 18px; border: none; border-radius: 15px; }"
        "QPushButton:hover { background-color: #45a049; }"
    )

    # Appliquer un style personnalisé au bouton d'actualisation
    bouton_actualiser_contact.setStyleSheet(
        "QPushButton { color: white; font-size: 14px; border: none; border-radius: 5px; }"
        "QPushButton:hover { background-color: #0b7dda; }"
    )
    #création de la zone de scroll qui aura une Vbox dedans contenant la liste des boutons des Contacts
    scroll_zone_contacts = QScrollArea(fenetre)
    scroll_zone_contacts.setGeometry(0, 100, Width, Height - 50)
    scroll_zone_contacts.setWidgetResizable(True)
    scroll_zone_contacts.show()

    actualiser_liste_contacts(scroll_zone_contacts,None)


def main():#appelé au debut du programme juste pour s'occuper de la fenetre et qui appelera le main_menu
    global app, fenetre
    app = QApplication(sys.argv)
    
    fenetre = QMainWindow()
    fenetre.setWindowTitle("Carnet d'adresses")
    fenetre.setGeometry(100, 100, Width, Height)  # Définit la position et la taille de la fenêtre
    fenetre.setCursor(Qt.PointingHandCursor)
    main_menu(fenetre)

    fenetre.show()
    sys.exit(app.exec_())

main()