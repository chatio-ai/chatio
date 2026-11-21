all:
	docker build --force-rm --progress plain -t localhost/chatio .

re:
	docker build --force-rm --progress plain --no-cache -t localhost/chatio .
