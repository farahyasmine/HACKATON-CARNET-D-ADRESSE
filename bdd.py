import sqlite3

def connect_database():
    conn = sqlite3.connect('carnet_adresses.db')
    cursor = conn.cursor()

    # Création de la table contacts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            idcontact INTEGER PRIMARY KEY AUTOINCREMENT,
            nom VARCHAR(255),
            prenom VARCHAR(255),
            surnom VARCHAR(255),
            entreprise VARCHAR(255),
            photo BLOB
        )
    ''')

    # Création de la table adresse
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS adresse (
            ida INTEGER PRIMARY KEY AUTOINCREMENT,
            idcontact INTEGER,
            codepostal INTEGER,
            ville VARCHAR(255),
            pays VARCHAR(255),
            nomrue VARCHAR(255),
            nbrue INTEGER,
            FOREIGN KEY (idcontact) REFERENCES contacts (idcontact)
        )
    ''')

    # Création de la table numeros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS numeros (
            idnum INTEGER PRIMARY KEY AUTOINCREMENT,
            idcontact INTEGER,
            numero VARCHAR(20),
            FOREIGN KEY (idcontact) REFERENCES contacts (idcontact)
        )
    ''')

    # Création de la table email
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email (
            idmail INTEGER PRIMARY KEY AUTOINCREMENT,
            idcontact INTEGER,
            adressemail VARCHAR(255),
            FOREIGN KEY (idcontact) REFERENCES contacts (idcontact)
        )
    ''')

    conn.commit()
    return conn, cursor

def modifier_contact(idcontact, nom, prenom, surnom, entreprise,photo, codepostal, ville, pays, nomrue, nbrue, numero, adressemail):
    conn, cursor = connect_database()

    # Modification du contact
    cursor.execute('''
        UPDATE contacts
        SET nom=?, prenom=?, surnom=?, entreprise=?, photo=?
        WHERE idcontact=?
    ''', (nom, prenom, surnom, entreprise,photo, idcontact))

    # Modification de l'adresse
    cursor.execute('''
        UPDATE adresse
        SET codepostal=?, ville=?, pays=?, nomrue=?, nbrue=?
        WHERE idcontact=?
    ''', (codepostal, ville, pays, nomrue, nbrue, idcontact))

    # Modification du numéro
    cursor.execute('''
        UPDATE numeros
        SET numero=?
        WHERE idcontact=?
    ''', (numero, idcontact))

    # Modification de l'email
    cursor.execute('''
        UPDATE email
        SET adressemail=?
        WHERE idcontact=?
    ''', (adressemail, idcontact))

    conn.commit()
    conn.close()

def ajouter_contact(nom, prenom, surnom,photo, entreprise, codepostal, ville, pays, nomrue, nbrue, numero, adressemail):
   try:
    conn, cursor = connect_database()
    # Ajout du contact
    cursor.execute('''
        INSERT INTO contacts (nom, prenom, surnom, entreprise,photo)
        VALUES (?, ?, ?, ?, ?)
    ''', (nom, prenom, surnom, entreprise, photo))
    
    idcontact = cursor.lastrowid  # Récupérer l'id du dernier contact ajouté

    # Ajout de l'adresse
    cursor.execute('''
        INSERT INTO adresse (idcontact, codepostal, ville, pays, nomrue, nbrue)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (idcontact, codepostal, ville, pays, nomrue, nbrue))

    print(f"Insertion du numéro {numero} pour le contact {idcontact}")

    # Ajout du numéro
    cursor.execute('''
        INSERT INTO numeros (idcontact, numero)
        VALUES (?, ?)
    ''', (idcontact, numero))

    # Ajout de l'email
    cursor.execute('''
        INSERT INTO email (idcontact, adressemail)
        VALUES (?, ?)
    ''', (idcontact, adressemail))
    conn.commit()
   except Exception as e:
        print(f"Erreur lors de l'ajout du contact : {e}")
   finally:
    conn.close()

def select_photo(idcontact):
    conn, cursor = connect_database()
    cursor.execute('''SELECT photo FROM contacts WHERE idcontact=?''', (idcontact,))
    photo = cursor.fetchall()
    conn.commit()
    conn.close()
    return photo


#on va decomposer ajouter_contact pour faciliter l'ajout d'un contact
def ajouter_contact_main(nom,prenom,surnom,photo,entreprise):
    conn, cursor = connect_database()
    # Ajout du contact
    cursor.execute('''INSERT INTO contacts (nom, prenom, surnom, entreprise,photo) VALUES (?, ?, ?, ?, ?)''', (nom, prenom, surnom, entreprise, photo))
    conn.commit()
    conn.close()
    return cursor.lastrowid #return l'id du contact créer

def ajouter_contact_adresse(idcontact,codepostal,ville,pays,nomrue,nbrue):
    conn, cursor = connect_database()
    cursor.execute('''
        INSERT INTO adresse (idcontact, codepostal, ville, pays, nomrue, nbrue)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (idcontact, codepostal, ville, pays, nomrue, nbrue))
    conn.commit()
    conn.close()

def ajouter_contact_numero(idcontact,numero):
    conn, cursor = connect_database()
    cursor.execute('''
        INSERT INTO numeros (idcontact, numero)
        VALUES (?, ?)
    ''', (idcontact, numero))
    conn.commit()
    conn.close()

def ajouter_contact_mail(idcontact,adressemail):
    conn, cursor = connect_database()
    cursor.execute('''
        INSERT INTO email (idcontact, adressemail)
        VALUES (?, ?)
    ''', (idcontact, adressemail))
    conn.commit()

def modifier_contact_main(idcontact,nom,prenom,surnom,photo,entreprise):
    conn, cursor = connect_database()
    # Modif du contact
    cursor.execute('''UPDATE contacts SET nom=?, prenom=?, surnom=?, entreprise=?, photo=? WHERE idcontact=?''', (nom, prenom, surnom, entreprise, photo, idcontact))
    conn.commit()
    conn.close()
    return cursor.lastrowid #return l'id du contact créer

def modifier_contact_adresse(ida,codepostal,ville,pays,nomrue,nbrue):
    print(ida,codepostal,ville,pays,nomrue,nbrue)
    conn, cursor = connect_database()
    cursor.execute('''UPDATE adresse SET codepostal=?, ville=?, pays=?, nomrue=?, nbrue=? WHERE ida=?''', (codepostal, ville, pays, nomrue, nbrue,ida))
    conn.commit()
    conn.close()

def modifier_contact_numero(idn,numero):
    conn, cursor = connect_database()
    cursor.execute('''UPDATE numeros SET numero=? WHERE idnum=?''',(numero,idn))
    conn.commit()
    conn.close()

def modifier_contact_mail(ide,adressemail):
    conn, cursor = connect_database()
    cursor.execute('''UPDATE email SET adressemail=? WHERE idmail=?''',(adressemail,ide))
    conn.commit()
    conn.close()

def supprimer_contact_main(idcontact):
    conn, cursor = connect_database()
    cursor.execute('DELETE FROM contacts WHERE idcontact=?', (idcontact,))
    conn.commit()
    conn.close()

def supprimer_contact_adresse(idcontact, ida):
    conn, cursor = connect_database()
    if ida is not None:
        cursor.execute('''DELETE FROM adresse WHERE ida=?''', (ida,))
    else:
        cursor.execute('''DELETE FROM adresse WHERE idcontact=?''', (idcontact,))
    conn.commit()
    conn.close()

def supprimer_contact_numero(idcontact, ide):
    conn, cursor = connect_database()
    if ide is not None:
        cursor.execute('''DELETE FROM numeros WHERE idnum=?''', (ide,))
    else:
        cursor.execute('''DELETE FROM numeros WHERE idcontact=?''', (idcontact,))
    conn.commit()
    conn.close()

def supprimer_contact_mail(idcontact, ide):
    conn, cursor = connect_database()
    if ide is not None:
        cursor.execute('''DELETE FROM email WHERE idmail=?''', (ide,))
    else:
        cursor.execute('''DELETE FROM email WHERE idcontact=?''', (idcontact,))
    conn.commit()
    conn.close()

def rechercher_contact(recherche): #pb avec la recherche : si on met plusieurs mots il suffit que le contact contienne un seul des mots
    conn, cursor = connect_database()
    if recherche is None or recherche.strip() == '':
        cursor.execute('''SELECT * FROM contacts''')
    else:    
        recherche = recherche.split() # on divise la chaîne de caractères en une liste qui aura dedans chaque mot de la chaîne de caractères
        requete = 'SELECT * FROM contacts WHERE '
        requetes_conditions = [] # on va utiliser un tableau avec toutes les requêtes qu'on va faire
        valeurs = []
        plusieursmots = False
        for mot in recherche:
            requetes_conditions = [] #on reset requetes_conditions car elle contient deja toutes les requetes précédente (si on ne le reset pas et que recherche contient deux mots alors il y aura 33 valeurs demandé et on en donnera que 22)
            if plusieursmots:
                requete = requete + ' AND '
            # Ajouter chaque champ avec LIKE dans les conditions de la requête
            requetes_conditions.extend([
                'nom LIKE ?', 'prenom LIKE ?', 'surnom LIKE ?', 'entreprise LIKE ?',
                'idcontact IN (SELECT idcontact FROM email WHERE adressemail LIKE ?)',
                'idcontact IN (SELECT idcontact FROM numeros WHERE numero LIKE ?)',
                'idcontact IN (SELECT idcontact FROM adresse WHERE codepostal LIKE ? OR ville LIKE ? OR pays LIKE ? OR nomrue LIKE ? OR nbrue LIKE ?)'
            ])
            
            # Ajouter chaque mot recherché pour chaque champ
            valeurs.extend([f'%{mot}%'] * 11)  # on met dans values l'ensemble des requêtes

            # on joins toutes les conditions avec des OR pour chaque mot (on rajoute AND à chaque fois pour que si il y a plusieurs mots ils soient nécéssaires dans le contact)
            requete = requete +'('+ ' OR '.join(requetes_conditions) +')'
            plusieursmots = True #permet juste d'ajouter à la prochaine itération de la boucle le AND entre chaque WHERE de chaque noms


        cursor.execute(requete, valeurs)  # on finit par envoyer la requête avec comme paramètre la liste des valeurs qui est juste tous les mots x10

    resultat = cursor.fetchall()
    conn.close()
    return resultat

def load_contact(idcontact): 
    conn, cursor = connect_database()
    cursor.execute('''SELECT * FROM contacts WHERE idcontact=?''', (idcontact,))
    contact_info = cursor.fetchall()

    cursor.execute('''SELECT * FROM adresse WHERE idcontact=?''', (idcontact,))
    adresse_info = cursor.fetchall()

    cursor.execute('''SELECT * FROM numeros WHERE idcontact=?''', (idcontact,))
    numeros_info = cursor.fetchall()

    cursor.execute('''SELECT * FROM email WHERE idcontact=?''', (idcontact,))
    email_info = cursor.fetchall()

    return contact_info, adresse_info, numeros_info, email_info

connect_database()