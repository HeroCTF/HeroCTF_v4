su player -c "node /home/player/server/server.js &"
service mysql start&
/bin/sh -c "/usr/sbin/apachectl -D FOREGROUND"