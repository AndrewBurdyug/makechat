.PHONY: run
run: createdirs touchfiles runmongo runbackend runweb

.PHONY: createdirs
createdirs:
	sudo mkdir /makechat-backups /var/lib/makechat-mongo
	sudo chmod 700 /makechat-backups /var/lib/makechat-mongo

.PHONY: touchfiles
touchfiles:
	sudo touch /etc/makechat.conf
	sudo chmod 600 /etc/makechat.conf

.PHONY: runmongo
runmongo:
	docker run -v /var/lib/makechat-mongo:/data/db --name makechat-mongo -d mongo:latest

.PHONY: runbackend
runbackend:
	docker run -v /etc/makechat.conf:/etc/makechat.conf -v /makechat-backups:/backups \
    --name makechat --link makechat-mongo:mongo-server -d buran/makechat:latest

.PHONY: rebuildweb
rebuildweb:
	docker stop makechat-web
	docker rm makechat-web
	docker rmi buran/makechat-web
	docker build -t buran/makechat-web --rm docker/makechat-web

.PHONY: runweb
runweb:
	docker run --name makechat-web --link makechat:backend-server -d buran/makechat-web:latest

.PHONY: stopall
stopall:
	docker stop makechat-web makechat makechat-mongo

.PHONY: rmall
rmall:
	docker rm makechat-web makechat makechat-mongo
