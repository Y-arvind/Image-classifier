FROM anibali/pytorch:1.13.1-cuda11.7-ubuntu22.04

WORKDIR /classifier

COPY requirements.txt /classifier
RUN sudo apt-get update
RUN sudo apt-get install -y libsm6 libxext6 libxrender-dev libglib2.0-0
RUN pip install -r requirements.txt

COPY . /classifier
RUN sudo chmod -R a+rwx /classifier/
EXPOSE 5000
CMD [ "python", "app.py" ]
