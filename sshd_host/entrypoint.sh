#!/bin/bash

if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
  echo "USERNAME or PASSWORD not set"
  exit 1
fi

useradd -m -s /bin/bash "$USERNAME"
echo "$USERNAME:$PASSWORD" | chpasswd
usermod -aG sudo "$USERNAME"

# Enable password auth
sed -i 's/^#*PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/^#*PermitRootLogin .*/PermitRootLogin no/' /etc/ssh/sshd_config

# Add scripts to PATH for all users
echo "export PATH=\$PATH:/usr/local/bin/scripts" >> /home/$USERNAME/.bashrc

# Start SSH daemon
/usr/sbin/sshd -D -e