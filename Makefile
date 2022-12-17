PORT=8080

start:
	docker build -t 411-app .
	export PORT=8080 && docker run -it --rm -p $(PORT):$(PORT) -e $$PORT 411-app 

develop:
	docker build -t 411-develop -f Dockerfile-develop .
	docker run -it --rm -p 8080:8080 -v `pwd`/flask-app:/flaskr 411-develop

build:
	docker build -t neilk3/411-flask:latest -f Dockerfile-build .

run:
	docker run -it --rm -p $(PORT):$(PORT) neilk3/411-flask:latest

push: 
	docker push neilk3/411-flask:latest

waitress:
	waitress-serve --port=$(PORT) --call app:create_app

# gcloud auth login
# gcloud config set project cs-411-final-project-342117
gcp-deploy:
	gcloud builds submit --tag gcr.io/cs-411-final-project-342117/ireserve
	gcloud run deploy --image gcr.io/cs-411-final-project-342117/ireserve --add-cloudsql-instances=cs-411-final-project-342117:us-central1:preql --platform managed