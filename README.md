# Fitness Club DBMS
A GUI application for a Health and Fitness Club Management System.
This system will serve as a platform catering to the needs of club members, trainers, and administrative staff.
Feel free to play around with it :)

### Project Report
• Conceptual Design: the ER-diagram for the Health and Fitness Club, and assumptions

• Reduction to Relation Schemas: consolidate ER-diagram into relational schemas using the most effective method for mapping ER components to tables.

• DDL File

• DML File

• Code Implementation in Python

### Prerequisites
If Python is not installed in your system, then you can install it by running the given command in your terminal:
```pip install python```

Open the command prompt (Windows) or the terminal (MacOS) and run the below command to install psycopg2:
```pip install psycopg2```

Download Management_System_GUI.py from my ```source``` folder.
Download DDL.sql and DML.sql from my ```SQL``` folder.

### Setting up in PosgreSQL
Login to pgAdmin 4 and create a new database with a name of your choice.
Go to Query tool => Open the DDL.sql and DML.sql scripts from local device => Execute.
Optionally, you can just run the Python program which will automatically create tables and set up the sample data.

### Compilation
You can run the Python program using your IDE or use the terminal:
```python Management_System_GUI.py```

Once the program is running, it'll promt you for the database name, pgAdmin 4 username, and password.
```Enter the database name: <name of database you created>```
```Enter your pgadmin 4 username: postgres```
```Enter your pgadmin 4 password: <your pgAdmin 4 password>```

### Demo
From 10:20 to 12:00, the audio does NOT sync up with the video. That section should still show that Group Events are created with the database updated successfully.
Youtube link: https://youtu.be/DNKNI7F-ztw
