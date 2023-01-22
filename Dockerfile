# set base image (host OS)
FROM python:3.8-slim

# update OS
RUN apt-get update && apt-get upgrade -y

# copy the app to container
ADD . /TeCBenchAPI

# set the working directory in the container
WORKDIR /TeCBenchAPI

# install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# command to run on container start
CMD python app.py

