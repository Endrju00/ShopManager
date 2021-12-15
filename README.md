# ShopManager


## Table of contents
* [General info](#general-info)
* [Database diagrams](#database-diagrams)
* [Technologies](#technologies)
* [First configuration](#first-configuration)

## General info
The application is used to manage the store. This system will enable the storage of information about products, their stock in the warehouse, orders from customers, information about customers, employees and wholesalers from which the store orders the goods. The user who uses the application will be able to define, view and edit this data. For example, it can enter information about new orders, products, and also change, for example, employee wages.

## Database diagrams

### Entity diagram
![](diagrams/entity_diagram/diagram_zwiazkow_encji.png)

### Relationship diagram
![](diagrams/relationship_diagram/schemat_relacyjny.png)

## Technologies
* Python
* Django
* HTML5
* CSS3

## First configuration
1. Install prerequisites
> pip install -r requirements.txt
2. [Download](https://downloads.mariadb.org/) and install MariaDB
3. Set password, name of the db and port in project/project/settings.py
4. Add new environment variable to Path: path_to\MariaDB 10.6\bin
5. Restart cmd and run
> mysql -u root -p
6. Create and configure database
> CREATE DATABASE shopmanager_db;
> 
> USE shopmanager_db;
7. Create function and procedure from diagrams/relationship_diagram/procedura_funkcja_mysql.sql
> CREATE OR REPLACE FUNCTION...
> 
> CREATE OR REPLACE PROCEDURE...
> 
> exit
9. Migrate
> python manage.py migrate
10. Run the application
> python manage.py runserver
