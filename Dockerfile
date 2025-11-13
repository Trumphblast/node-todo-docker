# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Make port 5000 available to the world outside this container
# This is the port Flask is running on (from app.py)
EXPOSE 5000

# Define environment variable placeholder
# We will pass the actual value in when we run the container
ENV MONGO_URI="mongodb+srv://kumarjbharath76:SriRam97337@cluster0.ismozuu.mongodb.net/?appName=Cluster0"

# Run app.py when the container launches
# We use "flask run" instead of "python app.py" to ensure it binds
# to 0.0.0.0, which is necessary inside a container.
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
