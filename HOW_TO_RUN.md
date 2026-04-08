# How to Run the Project

## 1. Start the Database
- Start PostgreSQL with Docker Compose:
  ```bash
  docker-compose up -d
  ```

## 2. Load Data (First Time or When CSV Changes)
- Download the HDB resale flat prices CSV from data.gov.sg and place it in `data/raw/hdb_resale_raw.csv`.
- Load the CSV into the database:
  ```bash
  python src/load_to_db.py
  ```

## 3. Transform Data
- Run the transformation script:
  ```bash
  python src/transform.py
  ```

## 4. Launch the Dash App
- Start the Dash web app:
  ```bash
  python app/main.py
  ```

## 5. Stop Everything
- To stop all services:
  ```bash
  docker-compose down
  ```

## One-Click Run (Linux/macOS)
- You can use the provided script to run everything:
  ```bash
  bash run_all.sh
  ```

---

- If you shut down your computer, just repeat steps 1 and 4 (and 2 if you update the CSV).
- The database persists in the `pgdata` Docker volume.
