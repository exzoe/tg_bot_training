import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден. Проверь файл .env")


def parse_admin_ids(admin_ids_raw: str | None) -> list[int]:
    if not admin_ids_raw:
        return []

    admin_ids = []

    for admin_id in admin_ids_raw.split(","):
        admin_id = admin_id.strip()

        if not admin_id:
            continue

        if not admin_id.isdigit():
            raise ValueError(
                "ADMIN_IDS должен содержать только числа через запятую. "
                "Например: ADMIN_IDS=123456789,987654321"
            )

        admin_ids.append(int(admin_id))

    return admin_ids


ADMIN_IDS = parse_admin_ids(os.getenv("ADMIN_IDS"))