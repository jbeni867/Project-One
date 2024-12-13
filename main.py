from tkinter import Tk
from logic import Logic


def main() -> None:
    window: Tk = Tk()
    window.title("ATM")
    window.geometry("500x500")
    window.resizable(False, False)
    Logic(window)
    window.mainloop()


if __name__ == "__main__":
    main()
