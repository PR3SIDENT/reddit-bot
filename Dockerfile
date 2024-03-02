FROM python:3.11.8-alpine

# Copy requirements and install into image
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy project into image
COPY . /app
WORKDIR /app

# Run bot.py
CMD ["python", "-u", "bot.py"]
