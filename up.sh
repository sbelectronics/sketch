ADDR=198.0.0.242
rsync -avz --exclude "__history" --exclude "*~" --exclude "home-pi-*" --exclude "dot*" --exclude "*.conf" --exclude "*.pyc" --exclude ".git" -e ssh . pi@$ADDR:/home/pi/etch-a-sketch
