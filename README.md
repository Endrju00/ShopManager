# Projekt-ZBD

### Szybka instalacja
1. Stwórz bazę danych <code>MariaDB</code>.
> mysql -u root -p

> create database shopmanager_db4;

> exit

2. Stwórz tabele zgodne ze [skryptem ddl](https://github.com/Endrju00/Projekt-ZBD/blob/main/diagrams/relationship_diagram/relacja.ddl).
> cd diagrams/relationship_diagram

> mysql -u root -p shopmanager_db4 < relacja.ddl
3. Wgraj procedurę i funkcję z [additional.sql](https://github.com/Endrju00/Projekt-ZBD/blob/main/diagrams/relationship_diagram/additional.sql).
> mysql -u root -p shopmanager_db4 < additional.sql
4. Stwórz wirtualne środowisko i zainstaluj biblioteki.
> cd ../../

>conda create --name zbd python=3.7

> conda activate zbd

> pip install -r requirements.txt
4. Uruchom projekt.
> cd project 

> python manage.py runserver
