# Use lightweight Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY requirements.txt .
COPY src/ ./src/
COPY data/ ./data/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit uses
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]