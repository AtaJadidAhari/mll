# Use Ubuntu 22 as the base image
FROM ubuntu:jammy

# Update the package lists
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

# Install Python 3.10 and pip
RUN apt-get install -y python3.10 python3-pip

# Make sure Python points to Python 3.10
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Set the working directory in the container
WORKDIR /home

RUN pip install --no-cache-dir dash dash_bootstrap_components numpy pandas gunicorn orjson dash_loading_spinners

RUN git clone https://github.com/AtaJadidAhari/mll.git

WORKDIR /home/mll 

EXPOSE 8080
# Command to run the Python application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--workers", "3", "--max-requests", "20", "--timeout", "120",  "wsgi"]

