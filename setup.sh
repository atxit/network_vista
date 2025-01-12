#sudo chown $(whoami):$(whoami) /var/run/docker.sock
python3 --version
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
echo "SETUP COMPLETE"