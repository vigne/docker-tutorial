# Use an official Python runtime as a parent image
FROM python

# Use pip to install dependencies
RUN pip install --trusted-host pypi.python.org redis flask

# Set the working directory to /app
WORKDIR /app

# Copy the example source directory contents into the container at /app
COPY ./src /app


# Set environment variable pointing to container-local libraries
ENV FLASK_APP /app/app.py

EXPOSE 5000

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
