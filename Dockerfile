FROM anibali/pytorch:1.5.0-cuda10.2

WORKDIR /classifier

COPY requirements.txt /classifier
RUN sudo apt-get update
RUN sudo apt-get install -y libsm6 libxext6 libxrender-dev libglib2.0-0
RUN pip install -r requirements.txt

COPY . /classifier
RUN sudo chmod -R a+rwx /classifier/
CMD [ "python", "app.py" ]
