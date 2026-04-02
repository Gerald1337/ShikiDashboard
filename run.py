from db import init_db, migrate_db, cleanup_old_service_checks
from checks import start_service_polling, background_drive_poll, background_cleanup
from app import app
import threading


def main():
    init_db()
    migrate_db()
    threading.Thread(target=background_drive_poll, daemon=True).start()
    threading.Thread(target=background_cleanup, daemon=True).start()
    try:
        cleanup_old_service_checks()
    except Exception:
        pass
    start_service_polling()
    print("\n Shiki Dashboard is running!")
    print("  Open http://localhost:8080 in your browser")
    print("  Service check history is automatically pruned every 12h (keeps last 24h)\n")
    app.run(host="0.0.0.0", port=8080, debug=False)


if __name__ == '__main__':
    main()
