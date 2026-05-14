import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import persistence

def test_save_and_get():
    persistence.init_db()
    persistence.save_result("Alice", "Bob", 25, 20)
    results = persistence.get_results()
    assert len(results) > 0
    print("Test passed: Result saved and retrieved")

if __name__ == "__main__":
    test_save_and_get()
