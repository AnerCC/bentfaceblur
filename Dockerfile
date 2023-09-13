# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE 5002

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN apt-get update && \ 
    apt-get install -y libgl1-mesa-glx
RUN apt-get update && \ 
    apt-get install -y libgl1-mesa-glx libglib2.0-0
RUN pip install --no-cache-dir opencv-python-headless
RUN pip install --no-cache-dir flask==2.3.0
RUN pip install --no-cache-dir gunicorn==20.1.0
RUN pip install --no-cache-dir retina-face==0.0.13
RUN pip install --no-cache-dir psutil

WORKDIR /app
COPY . /app


# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5000","--timeout", "360", "app.app:app"]
# CMD ["gunicorn", "--bind", "0.0.0.0:5002","--workers", "4", "app.app:app", "--preload", "--pythonpath", "."]
