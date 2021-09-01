import os


def delete_welcome_image(name: str) -> None:
    if (path :=
            f"./assets/welcome_images/{name}-welcome.png", os.path.exists(path)):
        os.remove(path)
