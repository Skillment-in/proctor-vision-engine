# main.py
from core.ProctoringEngine import ProctoringEngine

if __name__ == "__main__":
    print("🎯 Starting Proctor Vision Engine...")

    engine = ProctoringEngine(
        reference_image_path='reference.jpg',
        log_path='proctoring_log.json'
    )

    # ✅ Manual test log to verify logging works
    engine.flag_logger.log_violation("manual_test_violation")

    try:
        engine.start()
    except KeyboardInterrupt:
        print("🛑 Stopping engine...")
        engine.stop()
