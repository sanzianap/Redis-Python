# Redis-Python

J'ai utilise une table hash pour sauvegarder la base de donnees. 
Un utilisateur a une nombre de connexions n et n dates (heures) associes.
Quand on envoie une autre connexion, on verifie si on a des connexions expirees, si oui, on les efface et on sauvegarde la nouvelle si possible.
