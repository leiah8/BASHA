#!/bin/bash
# basha server setup — run once on a fresh Ubuntu/Debian VPS

set -e

apt-get update -q
apt-get install -y python3 python3-pip python3-venv ufw

useradd -m -s /bin/bash basha || true

mkdir -p /opt/basha
cp -r . /opt/basha/
chown -R basha:basha /opt/basha

cd /opt/basha
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

ufw allow 4444/tcp
ufw allow ssh
ufw --force enable

cp deploy/basha.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable basha
systemctl start basha

echo ""
echo "basha is running. nc <this-ip> 4444 to connect."
echo "she's been waiting."

