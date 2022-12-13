# Python interface

To setup the python interface you need to do the following in the ``python`` folder:
```bash
pip install -r requirements.txt
```
followed by:
```bash
python main.py
```

And you need to ssh into the VM and ensure there is data in the database with the following commands:
```bash
ssh bddst-g11-Node2 -L 10000:localhost:10000

docker exec -ti hive-server beeline

#username and password 'hive'
!connect jdbc:hive2://localhost:10000

SHOW TABLES;
```