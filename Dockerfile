# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD [ "python", "/cs3280project4.py" ]

# Add metadata to the image to describe which port the container is listening on at runtime.
EXPOSE 3280
