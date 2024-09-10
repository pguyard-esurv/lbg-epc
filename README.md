This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

# Getting started 

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
