import requests


BASE_URL = "http://127.0.0.1:5000"


def registrar_usuario():
    print("\n=== USER REGISTRATION ===")

    usuario = input("Username: ")
    contrasena = input("Password: ")

    response = requests.post(
        f"{BASE_URL}/registro",
        json={
            "usuario": usuario,
            "contraseña": contrasena
        }
    )

    print(f"\nStatus: {response.status_code}")
    print(response.json())


def iniciar_sesion():
    print("\n=== LOGIN ===")

    usuario = input("Username: ")
    contrasena = input("Password: ")

    response = requests.post(
        f"{BASE_URL}/login",
        json={
            "usuario": usuario,
            "contraseña": contrasena
        }
    )

    print(f"\nStatus: {response.status_code}")
    print(response.json())


def consultar_tareas():
    print("\n=== TASKS ===")

    response = requests.get(
        f"{BASE_URL}/tareas"
    )

    print(f"\nStatus: {response.status_code}")
    print(response.text)


def menu():
    while True:
        print("\n==============================")
        print(" TASK MANAGEMENT SYSTEM")
        print("==============================")
        print("1. Register user")
        print("2. Login")
        print("3. View tasks")
        print("4. Exit")

        opcion = input("\nSelect an option: ")

        if opcion == "1":
            registrar_usuario()

        elif opcion == "2":
            iniciar_sesion()

        elif opcion == "3":
            consultar_tareas()

        elif opcion == "4":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid option.")


if __name__ == "__main__":
    menu()