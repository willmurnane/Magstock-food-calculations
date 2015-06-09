help:
	@echo "build - Build container in production mode"
	@echo "run - Run container for in production mode"

build:
	docker build -t foodcalc .

run: build
	docker run -p=80:80 -t -i -v /opt/log:/sharedlogs foodcalc
