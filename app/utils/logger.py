import logging

def setup_logger():
    logging.basicConfig(
        filename="api.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def log_action(action: str, user: str, note_id: int = None):
    log_message = f"User: {user}, Action: {action}"
    if note_id:
        log_message += f", Note ID: {note_id}"
    logging.info(log_message)
