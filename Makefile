VERSION=$(shell cat VERSION)
PYVENV=$(shell which pyvenv)
VIRUTALENV=$(shell which virtualenv)
MAKECHAT_CT=$(shell docker ps -a --filter=\"ancestor=buran/makechat\" --format=\"{{.ID}}\")
MAKECHAT_CT_WEB=$(shell docker ps -a --filter=\"ancestor=buran/makechat-web\" --format=\"{{.ID}}\")

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
	if [ -f ~/makechat.conf ]; then sed -i "s/test_mode = off/test_mode = on/" ~/makechat.conf; fi
	docker restart makechat

.PHONY: testmodeoff
testmodeoff:
	docker exec -ti makechat sed -i "s/test_mode = on/test_mode = off/" /root/makechat.conf
	if [ -f ~/makechat.conf ]; then sed -i "s/test_mode = on/test_mode = off/" ~/makechat.conf; fi
	docker restart makechat

.PHONY: dotests
dotests:
	python tests/test_mongo.py -b -v
	python tests/test_auth.py -b -v
	python tests/test_tokens.py -b -v
	python tests/test_rooms.py -b -v

.PHONY: tests
tests: testmodeon dotests testmodeoff

.PHONY: createvenv
createvenv:
	if [ ! -d ~/envs ]; then mkdir -v ~/envs; fi

	if [ ! -z "$(PYVENV)" ]; then \
		pyvenv ~/envs/py3; \
	fi
	if [ ! -z "$(VIRUTALENV)" ]; then \
		if [ ! -d ~/envs/py3 ]; then \
			virtualenv -p python3 ~/envs/py3; \
		fi \
	fi
	if [ ! -z "$(PYVENV)" ] && [ ! -z "$(VIRUTALENV)" ]; then \
		echo "Can't create virtual environment, please install virtualenv!"; \
		exit 1; \
	fi

.PHONY: develop
develop: createvenv
	git pull
	. ~/envs/py3/bin/activate && python3 setup.py sdist
	. ~/envs/py3/bin/activate && pip install -e .

.PHONY: buildrelease
buildrelease:
	if [ ! -z $(MAKECHAT_CT) ]; then \
		docker stop $(MAKECHAT_CT); \
		docker rm $(MAKECHAT_CT); \
		docker rmi buran/makechat; \
	fi
	if [ ! -z $(MAKECHAT_CT_WEB) ]; then \
		docker stop $(MAKECHAT_CT_WEB); \
		docker rm $(MAKECHAT_CT_WEB); \
		docker rmi buran/makechat-web; \
	fi
	. ~/envs/py3/bin/activate && python3 setup.py sdist
	git commit -am 'Bump to version v$(VERSION)'
	git tag -a v$(VERSION) -m 'Version $(VERSION)'
	git push github
	git push github --tags
	twine upload dist/makechat-$(VERSION).tar.gz
	docker build -t buran/makechat --rm docker/makechat
	docker build -t buran/makechat-web --rm docker/makechat-web
	docker push buran/makechat
	docker push buran/makechat-web

.PHONY: newrelease
newrelease: buildrelease runbackend runweb tests

