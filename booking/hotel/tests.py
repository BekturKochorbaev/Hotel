import requests

BASE_URL = "http://localhost:8000/api/"  # можно заменить на prod URL через переменную окружения

def test_user_registration_and_login():
    print("🧪 Testing user registration and JWT login...")

    # Шаг 1: регистрация
    reg_data = {
        "username": "apitestuser",
        "email": "apitestuser@example.com",
        "password1": "VeryStrongPass123!",
        "password2": "VeryStrongPass123!"
    }
    r = requests.post(BASE_URL + "dj-rest-auth/registration/", json=reg_data)
    assert r.status_code == 201, f"Registration failed: {r.text}"
    print("✅ Registration passed")

    # Шаг 2: логин
    login_data = {
        "email": reg_data["email"],
        "password": reg_data["password1"]
    }
    r = requests.post(BASE_URL + "dj-rest-auth/login/", json=login_data)
    assert r.status_code == 200, f"Login failed: {r.text}"
    token = r.json()["access"]
    print("✅ Login passed")

    return token


def test_review_creation(token: str):
    print("🧪 Testing review creation...")
    headers = {"Authorization": f"Bearer {token}"}
    # Замените ID отеля, если нужно
    review_data = {
        "text": "Fantastic hotel from API test!",
        "stars": 5,
        "hotel": 1  # ID существующего отеля
    }
    r = requests.post(BASE_URL + "review_create/", json=review_data, headers=headers)
    assert r.status_code == 201, f"Review creation failed: {r.text}"
    print("✅ Review creation passed")


def test_booking_creation(token: str):
    print("🧪 Testing booking creation...")
    headers = {"Authorization": f"Bearer {token}"}
    booking_data = {
        "room": 1,  # ID существующей комнаты
        "check_in": "2025-07-01",
        "check_out": "2025-07-05"
    }
    r = requests.post(BASE_URL + "booking/", json=booking_data, headers=headers)
    assert r.status_code == 201, f"Booking failed: {r.text}"
    print("✅ Booking creation passed")


if __name__ == "__main__":
    token = test_user_registration_and_login()
    test_review_creation(token)
    test_booking_creation(token)
