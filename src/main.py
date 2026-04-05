from src.backend.backend import Backend
from src.frontend.frontend import Frontend

def main():
    backend = Backend()
    backend.start()

    frontend = Frontend(backend)

    frontend.run()


if __name__ == "__main__":
    main()