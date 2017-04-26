#!/usr/bin/env bash 
#We won't be using this, we just need a stub
apt-get install ruby -y
echo -e 'password\npassword\n' | sudo passwd root
sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
service ssh restart
