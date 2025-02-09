FROM python:3.9-slim

# Install Graphviz system dependencies
RUN apt-get update && apt-get install -y \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /sandbox

COPY sandbox/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY sandbox/sandbox.py /sandbox/sandbox.py
COPY question_generation /sandbox/question_generation
COPY utils /sandbox/utils
COPY models /sandbox/models

CMD ["python", "sandbox.py"]