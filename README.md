# Overview

This is a web app (Flask back end - React front end) which presents a form to LBG customers to sign up for an EPC.

The customer clicks on a link on an LBG site, which directs them to the back end of this web app. The back end verifies that the token which was passed with the request is valid via an API provided by LBG. After verification, it redirects the customer to the React app.

The customer enters their information in the form and submits it. In order to enter their address, the customer first enters their postcode in a postcode search which then queries a separate esurv Postgres instance which returns all addresses associated with the postcode.

The customer is then presented with some terms to accept, which are different depending on whether the address is in Scotland or not.

After the terms are accepted, the customer information is passed to the back end and the back end then sends the customer information via an API to SurveyHub if the customer is located in Scotland and ehouse if not in order to book the EPC.

The back end then records the customer information in a Postgres database.

# Getting started 

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

<p>The below code composes the project using a dockerfile which builds the React front end and then serves them up using a Flask server.</p>

```docker
docker build -f Dockerfile.combo -t react-flask-app .
```
> There are multiple Dockerfile in the directory (client only, api only, etc) so we specify the -f flag followed by the file name 

>-t flag is the tag of the docker image by default this is react-flask-app but should be renamed appropriately to reflect your image. 

<p>Once the container is built, it should be run using</p>

```docker
docker run --rm -p 3000:3000 react-flask-app
```

>The --rm flag instructs docker to clean up the container and remove system files upon container exit. Omit this flag when debugging to be able to see final state of container 

>The -p flag is the port the container is running, the left hand port is the docker host port and the right most port is the exposed port on the container. This needs to match the port being run as part of the flask server in the Dockerfile itself, by default this is 3000 on both. 


# External API Auth
**LBG Token API**: We are provided with an API key for both dev and prod.

**SurveyHub API**: We are provided with an API key for both dev and prod.

**ehouse API**: We are provided with a username and password which can be used to retrieve an authorization token. The API url is the same for dev and prod, but the username and password are different for each environment.

**Important and undocumented**: The ehouse API server does not provide the intermediate certificate in its SSL configuration so it was necessary to create a custom combined CA bundle which includes the DigiCert Global Root G2 (root certificate) and the RapidSSL TLS RSA CA G1 (intermediate certificate). This file is located at api\custom_ca_bundle.pem and since it is a public key it is included in the repo.

# External API Documentation

**LBG Token API**:

There is a swagger file located in the docs folder of this repo.

**SurveyHub API**: 

https://esurv.surveyhubuat.net/externalapi/swagger/index.html

**ehouse API**:

The API documentation can be found here: https://api.ehouse.co.uk/ 

Code snippets and more documentation (beta): https://documenter.getpostman.com/view/3010299/7LgEmAg#3f1d45b1-0c8c-8bdd-713c-84380dcf87e2 

Swagger: https://api.ehouse.co.uk/swagger/ui/index 
 
You can also log into the ehouse portal, if you want to add/view orders manually while setting up: https://portal.ehouse.co.uk/

# Secrets

# Database

# Deployment