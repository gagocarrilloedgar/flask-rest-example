rm -R -f ./migrations &&
pipenv run init &&
mysql -u root -e "DROP DATABASE example;" &&
mysql -u root -e "CREATE DATABASE example";
pipenv run migrate &&
pipenv run upgrade
