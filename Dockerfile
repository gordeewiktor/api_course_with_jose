# Use official Python image
FROM python:3.13

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire application code to the working directory
COPY . .

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Expose port 5001 instead
EXPOSE 5001

# Run the application on port 5001 instead of 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]