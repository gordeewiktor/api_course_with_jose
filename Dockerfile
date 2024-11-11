# Use official Python image
FROM python:3.13

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the entire application code to the working directory
COPY . .

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Run the application on port 5001 instead of 5000
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]