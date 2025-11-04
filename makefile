all:
	docker build --force-rm --progress plain -t chatio/chatio .

re:
	docker build --force-rm --progress plain --no-cache -t chatio/chatio .
