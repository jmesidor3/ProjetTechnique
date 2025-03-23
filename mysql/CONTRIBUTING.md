# pour ajouter les donnees
""" 
python3 dbMigration.py
# pour visualiser
"""""
docker exec -it mysql bash -l


docker run mysql  mysql -h mysql -u root -ppassword

use gestion_bibliotheque;


delete from auteur;
delete from categorie;
delete from livreauteur;
delete from livrecategorie;
delete from livre;
delete from editeur;



exit

 set foreign_key_checks=0;
drop table livreauteur, livrecategorie, livre, editeur, auteur, categorie;
drop database gestion_bibliotheque;
set foreign_key_checks=1


# Pour detruire les conteneurs
"""
docker compose down --remove-orphans --volumes --rmi=local
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
docker system prune -f
docker volume prune -f


sudo su
service docker stop
cd /var/lib/docker
rm -rf *
service docker start