from pathlib import Path

# Root folder for DB
PROJ = Path(__file__).parent
MAX_RESULTS  = 10 #default number of results

MODEL_NAME   = "unsloth/llama-3-8b-Instruct-bnb-4bit" #default model

DB_FILE      = "papers.db" # default database file
DB_PATH      = PROJ / DB_FILE