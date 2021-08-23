# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 8080

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# USER root

# RUN apt-get update
# RUN apt-get -y install cron

# Copy hello-cron file to the cron.d directory
# COPY scheduler /etc/cron.d/scheduler

# Give execution rights on the cron job
# RUN chmod 0644 /etc/cron.d/scheduler

# Apply cron job
# RUN crontab /etc/cron.d/scheduler
# RUN cron

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

RUN chmod a+x wait-for-it.sh

# CMD ["cron", "-f"]

# RUN chmod a+x run.sh
# CMD ["./run.sh"]
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
