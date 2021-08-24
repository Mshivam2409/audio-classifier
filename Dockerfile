FROM tensorflow/tensorflow  
RUN pip install flask
WORKDIR /root
COPY ./ ./
EXPOSE 5000