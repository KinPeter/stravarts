FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the files
COPY . .

# Expose port
EXPOSE 5400

# Run the FastAPI app
CMD ["fastapi", "run", "main.py", "--port", "5400"]