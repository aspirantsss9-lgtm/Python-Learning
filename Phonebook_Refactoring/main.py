from controller.controller import Controller


def main() -> None:
    """Application entry point."""

    controller = Controller()
    controller.run()


if __name__ == "__main__":
    main()