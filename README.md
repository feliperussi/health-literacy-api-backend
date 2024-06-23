# Health Literacy API

## Description
This project is a FastAPI application for health literacy analysis.

## Requirements
- Docker
- Docker Compose (optional)

## Setup Instructions

### Using Docker

1. **Build the Docker image:**

    ```sh
    docker build -t health-literacy-api .
    ```

2. **Run the Docker container:**

    ```sh
    docker run -p 8000:8000 health-literacy-api
    ```

3. **Access the API:**
    Open your browser and navigate to `http://127.0.0.1:8000`

### Local Development

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-repo/health-literacy-api.git
    cd health-literacy-api
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Download spaCy model:**

    ```sh
    python -m spacy download en_core_web_sm
    ```

5. **Run the application:**

    ```sh
    uvicorn main:app --reload
    ```

6. **Access the API:**
    Open your browser and navigate to `http://127.0.0.1:8000`

## Updating the Docker Container

1. **Stop the running container:**

    ```sh
    docker stop <container_id>
    ```

    Replace `<container_id>` with the actual container ID. You can find the container ID by running `docker ps`.

2. **Remove the old container:**

    ```sh
    docker rm <container_id>
    ```

3. **Build the updated Docker image:**

    ```sh
    docker build -t health-literacy-api .
    ```

4. **Run the updated Docker container:**

    ```sh
    docker run -p 8000:8000 health-literacy-api
    ```

Certainly! Here's the `API Endpoints` section in markdown code:

## API Endpoints

### Predict Readability with EMD Model

- **Endpoint:** `/comment/predict/model_emd`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "text": "<Your text here>"
  }
  ```
- **Response:**
  ```json
  {
    "prediction": 1,
    "score_plain": {...},
    "score_no_plain": {...}
  }
  ```

### Predict Readability with RF Model

- **Endpoint:** `/comment/predict/model_rf`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "text": "<Your text here>"
  }
  ```
- **Response:**
  ```json
  {
    "prediction": 1,
    "score_plain": {...},
    "score_no_plain": {...}
  }
  ```

### Predict Readability with GB Model

- **Endpoint:** `/comment/predict/model_gb`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "text": "<Your text here>"
  }
  ```
- **Response:**
  ```json
  {
    "prediction": "1",
    "score_plain": {...},
    "score_no_plain": {...}
  }
  ```

### Get Scoring

- **Endpoint:** `/comment/scoring`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "text": "<Your text here>"
  }
  ```
- **Response:**
  ```json
  {
    "readability_grades": {...},
    "sentence_info": {...},
    "word_usage": {...},
    "sentence_beginnings": {...}
  }
  ```

### Get Distributions

- **Endpoint:** `/comment/distributions`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "text": "<<Your text here>>"
  }
  ```
- **Response:**
  ```json
  {
    "total_words": 100,
    "total_sentences": 10,
    "total_characters": 500,
    ...
  }
  ```

### Get Readability

- **Endpoint:** `/comment/readability`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "text": "<Your text here>"
  }
  ```
- **Response:**
  ```json
  {
    "readability": {
      "Kincaid": 12.4,
      "ARI": 10.3,
      ...
    }
  }
  ```
