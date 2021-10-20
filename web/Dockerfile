#using a python3 image
FROM python:3
#changing to dictionary /usr/src/app
WORKDIR /usr/src/app
#copying requirements.txt to current dir /usr/src/
COPY requirements.txt ./
#run pip install for all library in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
#copying every thing from folder same as this Dockerfile
COPY . .
#executing the app.py with python
CMD [ "python", "app.py" ]
