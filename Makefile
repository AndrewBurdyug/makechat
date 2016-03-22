VERSION=$(shell cat VERSION)

.PHONY: run
run: createdirs createnetwork runmongo runbackend runweb add2hosts

.PHONY: createdirs
createdirs:
	sudo mkdir -pv /makechat-backups /var/lib/makechat-mongo /var/www/makechat
	sudo chmod 700 /makechat-backups /var/lib/makechat-mongo

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
	docker run --net=makechat_nw --ip=172.30.1.2 -v /makechat-backups:/backups \
	--name makechat -d buran/makechat:latest

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

.PHONY: pushbackend
pushbackend:
	python3 setup.py sdist
	sudo cp dist/makechat-$(VERSION).tar.gz /makechat-backups/
	docker exec -ti makechat pip install -U /backups/makechat-$(VERSION).tar.gz
	docker restart makechat

.PHONY: stopall
stopall:
	docker stop makechat-web makechat makechat-mongo

.PHONY: startall
startall:
	docker start makechat-mongo makechat makechat-web

.PHONY: rmall
rmall:
	docker rm makechat-web makechat makechat-mongo

.PHONY: testmodeon
testmodeon:
	docker exec -ti makechat sed -i "s/test_mode = off/test_mode = on/" /root/makechat.conf
	docker restart makechat

.PHONY: testmodeoff
testmodeoff:
	docker exec -ti makechat sed -i "s/test_mode = on/test_mode = off/" /root/makechat.conf
	docker restart makechat

.PHONY: dotests
dotests:
	python tests/test_mongo.py -b -v
	python tests/test_auth.py -b -v

.PHONY: tests
tests: testmodeon dotests testmodeoff
