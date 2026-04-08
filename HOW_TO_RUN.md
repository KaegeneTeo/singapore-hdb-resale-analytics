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

---

## Commit Message Conventions

Use the following types for your commit messages (Conventional Commits):

- **feat:**     A new feature (e.g. `feat: add dashboard tab for map`)
- **fix:**      A bug fix (e.g. `fix: correct price calculation logic`)
- **docs:**     Documentation only changes (e.g. `docs: update README with setup steps`)
- **style:**    Changes that do not affect meaning (whitespace, formatting, etc.)
- **refactor:** Code change that neither fixes a bug nor adds a feature (e.g. `refactor: simplify data pipeline`)
- **perf:**     Performance improvement (e.g. `perf: speed up CSV loading`)
- **test:**     Adding or correcting tests (e.g. `test: add test for transform_hdb_data`)
- **chore:**    Maintenance tasks (e.g. `chore: update dependencies`)

Example:
```
feat: add support for remaining_lease derivation
fix: handle missing values in combine script
```
