# init_db.py

from data.models.models_db import Base, Poster, Disko, User
from data.models.database import engine, SessionLocal

# Создаём таблицы (если нет)
print("Создаём таблицы...")
Base.metadata.drop_all(bind=engine)   # удаляем старые таблицы (осторожно! если не хочешь удалять данные, убери эту строку)
Base.metadata.create_all(bind=engine)

# Заполняем данными
db = SessionLocal()

posters = [
    Poster(name="Космическая принцесса", author="Lil Angelina", price=1500, size=1920, edition="матовый, без рамки", poster_url="https://picsum.photos/id/104/400/500"),
    Poster(name="Ангел в городе", author="Lil Angelina", price=2000, size=2160, edition="глянец, в рамке", poster_url="https://picsum.photos/id/20/400/600"),
    Poster(name="Nocturne", author="Lil Angelina", price=2400, size=1440, edition="холст на подрамнике", poster_url="https://picsum.photos/id/42/400/480"),
    Poster(name="Мечтательница", author="Lil Angelina", price=3200, size=2520, edition="лимитированная серия", poster_url="https://picsum.photos/id/169/400/650"),
]

disks = [
    Disko(album_name="Midnight Dreams", author="Lil Angelina", price=2500, edition="золотой винил", album_cover_url="https://picsum.photos/id/312/400/400", about={"year": 2024}),
    Disko(album_name="Neon Angel", author="Lil Angelina", price=2200, edition="серебряный винил", album_cover_url="https://picsum.photos/id/22/400/400", about={"year": 2023}),
]

users = [
    User(username="ivan_petrov", phone="+79991112233", mail="ivan@example.com", adres="ул. Ленина, д.1, кв.5"),
    User(username="maria_sidorova", phone="+79992223344", mail="maria@example.com", adres="пр. Мира, д.10, кв.20"),
]

db.add_all(posters + disks + users)
db.commit()
print(f"Добавлено постеров: {len(posters)}, дисков: {len(disks)}, пользователей: {len(users)}")
db.close()