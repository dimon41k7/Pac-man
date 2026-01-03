import pickle
import os

FILE = "records.bin"

def load_records():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "rb") as f:
            return pickle.load(f)
    except (EOFError, pickle.UnpicklingError):
        return []

def save_record(name, level, score):
    records = load_records()

    records.append({
        "name": name,
        "level": level,
        "score": score
    })

    records.sort(key=lambda r: r["score"])

    with open(FILE, "wb") as f:
        pickle.dump(records, f)