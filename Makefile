.PHONY: run
run: createdirs touchfiles createnetwork runmongo runbackend runweb add2hosts

.PHONY: createdirs
createdirs:
	sudo mkdir -pv /makechat-backups /var/lib/makechat-mongo /var/www/makechat
	sudo chmod 700 /makechat-backups /var/lib/makechat-mongo

.PHONY: touchfiles
touchfiles:
	sudo touch /etc/makechat.conf
	sudo chmod 600 /etc/makechat.conf

.PHONY: add2hosts
add2hosts:
	echo "172.30.1.1 makechat-mongo" | sudo tee --append /etc/hosts
	echo "172.30.1.2 makechat" | sudo tee --append /etc/hosts
	echo "172.30.1.3 makechat-web" | sudo tee --append /etc/hosts

.PHONY: createnetwork
createnetwork:
	docker network create -d bridge --subnet 172.30.0.0/16 makechat_nw

.PHONY: runmongo
runmongo:
	docker run --net=makechat_nw --ip=172.30.1.1 -v /var/lib/makechat-mongo:/data/db \
	--name makechat-mongo -d mongo:latest

.PHONY: runbackend
runbackend:
	docker run --net=makechat_nw --ip=172.30.1.2 -v /etc/makechat.conf:/etc/makechat.conf \
	-v /makechat-backups:/backups --name makechat -d buran/makechat:latest

.PHONY: runweb
runweb:
	docker run --net=makechat_nw --ip=172.30.1.3 --name makechat-web \
	-v /var/www/makechat:/usr/share/nginx/html/makechat/custom \
	-d buran/makechat-web:latest

.PHONY: rebuildweb
rebuildweb:
	docker stop makechat-web
	docker rm makechat-web
	docker rmi buran/makechat-web
	docker build -t buran/makechat-web --rm docker/makechat-web

.PHONY: rebuildbackend
rebuildbackend:
	docker stop makechat
	docker rm makechat
	docker rmi buran/makechat
	docker build -t buran/makechat --rm docker/makechat

.PHONY: stopall
stopall:
	docker stop makechat-web makechat makechat-mongo

.PHONY: startall
startall:
	docker start makechat-mongo makechat makechat-web

.PHONY: rmall
rmall:
	docker rm makechat-web makechat makechat-mongo
