FROM python:3.12.5

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Required to install PostgreSQL client
RUN apt-get update \
  && apt-get install python3-dev libpq-dev gcc -y

# Install pipenv
RUN pip install --upgrade pip 

# Install application dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the application files into the image
COPY . /app/

# Expose port 8000
EXPOSE 8000
