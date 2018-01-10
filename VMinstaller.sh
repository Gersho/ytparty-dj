#!/bin/bash
echo Enter the IP of the destination machine
read target
echo Enter the destination machine username
read username

ssh -t $username@$target -oStrictHostKeyChecking=no "sudo apt -y install python3-pip python3-venv apache2 libapache2-mod-wsgi-py3; mkdir ~/projects; exit"
scp -r ytparty/ requirements.txt environment 000-default.conf $username@$target:~/projects
ssh -t $username@$target -oStrictHostKeyChecking=no "cd ~/projects; sudo mv 000-default.conf /etc/apache2/sites-available/000-default.conf; python3 -m venv venv-ytparty; cat environment >> ~/projects/ytparty/ytparty/wsgi.py; chmod 664 ~/projects/ytparty/db.sqlite3; sudo chown :www-data ~/projects/ytparty/db.sqlite3; sudo chown :www-data ~/projects/ytparty; sudo service apache2 restart;. venv-ytparty/bin/activate; pip install -r requirements.txt; cd ytparty; python3 manage.py makemigrations; python3 manage.py migrate;  sudo service apache2 restart; exit"
