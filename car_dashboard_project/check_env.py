# check_env.py
with open(".env", "rb") as f:
    data = f.read()

try:
    text = data.decode("utf-8")
    print("✅ Файл .env в порядке (UTF-8 без ошибок)")
except UnicodeDecodeError as e:
    print("❌ Ошибка кодировки .env")
    print(f"Проблемный байт: {data[e.start:e.end]} (позиция {e.start})")