# Overview

This is a web app (Flask back end - React front end) which presents a form to LBG customers to sign up for an EPC.

The customer clicks on a link on an LBG site, which directs them to the back end of this web app. The back end verifies that the token which was passed with the request is valid via an API provided by LBG. After verification, it redirects the customer to the React app.

The customer enters their information in the form and submits it.

The customer is then presented with some terms to accept, which are different depending on whether the address is in Scotland or not.

After the terms are accepted, the customer information is passed to the back end and the back end then sends the customer information via an API to SurveyHub if the customer is located in Scotland and ehouse if not in order to book the EPC.

The back end then records the customer information in a Postgres database.

# Development 


# External API Auth
**LBG Token API**: We are provided with an API key for both dev and prod.

**SurveyHub API**: We are provided with an API key for both dev and prod.

**ehouse API**: We are provided with a username and password which can be used to retrieve an authorization token. The API url is the same for dev and prod, but the username and password are different for each environment.

**Important and undocumented**: The ehouse API server does not provide the intermediate certificate in its SSL configuration so it was necessary to create a custom combined CA bundle which includes the DigiCert Global Root G2 (root certificate) and the RapidSSL TLS RSA CA G1 (intermediate certificate). This file is located at api\custom_ca_bundle.pem and since it is a public key it is included in the repo.

To recreate the file, get the data from:

DigiCert Global Root G2 (Root Certificate): https://cacerts.digicert.com/DigiCertGlobalRootG2.crt.pem \
RapidSSL TLS RSA CA G1 (Intermediate Certificate): https://cacerts.digicert.com/RapidSSLTLSRSACAG1.crt.pem

Paste the info from the root certificate first and the info from the intermediate certificate second.

Each should be between:

-----BEGIN CERTIFICATE-----\
-----END CERTIFICATE-----

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
The username and password for the portal are located on the secret server under ehouse Portal Username and Password

# Secrets

# Database

The logging database for the web app is a Postgres database (psql-lbgepc-prd-uks-01) hosted on Azure alongside the web app. The logs for completed jobs are found on the data table lbg_epc_complete.

To run psql, from DEV-RPALINUX-01 enter:

```
psql "host=10.180.10.132 port=5432 dbname=postgres user=psqladmin"
```

You will then be prompted for the password. The password is located in the secret server under psql-lbgepc-prd-uks-01.

The address and signature data can be quite large fields, so the following can be a useful query:


    SELECT
        date, z_ref, full_name, phone_number, api_call, todays_date, complete,
        CASE
            WHEN signature_data IS NULL OR signature_data = '' THEN 'Empty'
            ELSE 'Has Data'
        END AS signature_data_status,
        CASE
            WHEN address IS NULL OR address = '' THEN 'Empty'
            ELSE 'Has Data'
        END AS address_status
    FROM
        lbg_epc_complete;

In order to extract a signature (in case of audit etc), from DEV-RPALINUX-01 enter:

    python3 api/signature_check.py <z_ref>

The signature will be downloaded from the database as a png in the format api/<z_ref>_signature.png

In lieu of other methods, the repo can be pulled to your local machine to access the png file.

# Deployment

The site is deployed as an Azure web app.

Resource group: rg-lbgepc-prd-uks-01
Web app: wa-lbgepc-prd

The URL for the site is https://lbg-epc.esurv.co.uk/ but the site cannot be accessed without a token provided by LBG in the format https://lbg-epc.esurv.co.uk/?token=

To update the app:

DEV-RPALINUX-01 is being used as a staging area (Repos/lbg-epc)

Push the latest copy to the repo, then run the following commands:

    docker build -t epc -f Dockerfile.prod .
    docker image tag epc azacresurv.azurecr.io/lbg-epc:latest
    docker login azacresurv.azurecr.io
    docker push azacresurv.azurecr.io/lbg-epc:latest

Then restart the app in Azure (you will likely need to be given permissions for the resource group, as well as an az_admin account if you don't have one yet).

# Future considerations

Email RPA

Z references

ehouse SSL certificate
