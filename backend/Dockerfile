# Use an official Python runtime as a parent image
FROM python:3.12-bookworm AS builder
# Set the working directory in the container
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
#RUN --mount=type=cache,target=/root/.cache/pip \
#   pip3 install -r requirements.txt
COPY . /app
# Install any needed packages specified in requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
# Make port 4000 available to the world outside this container
#EXPOSE 4000
# Run main.py when the container launcher
#ENV HOST=172.17.67.237
ENTRYPOINT ["python3"]
CMD ["main.py"]