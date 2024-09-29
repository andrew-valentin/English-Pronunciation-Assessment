# Use an official Python 3.9 image as the base
FROM python:3.9-slim

EXPOSE 8080

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the app code
COPY . .

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8080", "--server.address=0.0.0.0"]