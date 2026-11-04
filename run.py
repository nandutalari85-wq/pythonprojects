import os
import sys
from app import create_app
from app.models import db

app = create_app(os.getenv("FLASK_ENV", "development"))


def initialize_environment():
    """Verify database connectivity and create tables on startup."""
    with app.app_context():
        try:
            db.create_all()
            print(">> Database tables verified and ready.")
        except Exception as e:
            print("\n" + "=" * 70)
            print(">> DATABASE CONNECTION WARNING:")
            print(f">> {str(e)}")
            print(">> If you have not started MySQL Server yet:")
            print(">> 1. Start your MySQL service: 'net start MySQL80'")
            print(">> 2. Or set 'USE_SQLITE=true' in your .env file to run instantly with SQLite.")
            print("=" * 70 + "\n")


if __name__ == "__main__":
    initialize_environment()
    port = int(os.getenv("PORT", 5000))
    print(f"\n>> Agricultural Crop Production Analysis System running at: http://127.0.0.1:{port}/\n")
    app.run(host="127.0.0.1", port=port, debug=True)
