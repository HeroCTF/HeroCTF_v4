service mysql start
mysql -e "CREATE DATABASE user_db /*\!40100 DEFAULT CHARACTER SET utf8 */;"
mysql -e "CREATE USER player@localhost IDENTIFIED BY 'd4AP?5RB7k5My68';"
mysql -e "GRANT SELECT ON user_db.* TO 'player'@'localhost' IDENTIFIED BY 'd4AP?5RB7k5My68';"
mysql -e "FLUSH PRIVILEGES;"
mysql user_db < /home/player/server/database/schema.sql