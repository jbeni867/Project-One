from tkinter import Tk, Frame, Label, Entry, IntVar, Radiobutton, Button


class Gui:
    def __init__(self, window: Tk):
        self.window: Tk = window

        self.frame_first: Frame = Frame(window)
        self.label_first_name: Label = Label(self.frame_first, text="First Name:")
        self.field_first_name: Entry = Entry(self.frame_first)
        self.label_first_name.pack(side="left")
        self.field_first_name.pack(side="right", padx=10)
        self.frame_first.pack(anchor="center", padx=10, pady=10)

        self.frame_last: Frame = Frame(window)
        self.label_last_name: Label = Label(self.frame_last, text="Last Name:")
        self.field_last_name: Entry = Entry(self.frame_last)
        self.label_last_name.pack(side="left")
        self.field_last_name.pack(side="right", padx=10)
        self.frame_last.pack(anchor="center", padx=10, pady=10)

        self.frame_pin: Frame = Frame(window)
        self.label_pin: Label = Label(self.frame_pin, text="Pin Number:")
        self.field_pin: Entry = Entry(self.frame_pin, show="*")
        self.label_pin.pack(
            side="left",
        )
        self.field_pin.pack(side="right", padx=10)
        self.frame_pin.pack(anchor="center", padx=10, pady=10)

        self.frame_account_type: Frame = Frame(self.window)
        self.label_prompt: Label = Label(
            self.frame_account_type, text="Select Account Type"
        )
        self.radio_account_choice: IntVar = IntVar()
        self.radio_account_choice.set(0)
        self.radio_checking: Radiobutton = Radiobutton(
            self.frame_account_type,
            text="Checking",
            variable=self.radio_account_choice,
            value=1,
        )
        self.radio_savings: Radiobutton = Radiobutton(
            self.frame_account_type,
            text="Saving",
            variable=self.radio_account_choice,
            value=2,
        )
        self.label_prompt.pack(side="left", padx=5)
        self.radio_checking.pack(side="left")
        self.radio_savings.pack(side="left")
        self.frame_account_type.pack(anchor="center", pady=10)

        self.label_alert: Label = Label(self.window)
        self.label_balance: Label = Label(self.window)

        self.button_submit: Button = Button(
            self.window, text="LOGIN", command=self.setup_gui
        )
        self.button_submit.pack(anchor="center", pady=10)

        self.frame_transaction: Frame = Frame(self.window)
        self.label_transaction_type: Label = Label(
            self.frame_transaction, text="Select Transaction Type"
        )
        self.radio_transaction_type: IntVar = IntVar()
        self.radio_transaction_type.set(0)
        self.radio_withdraw: Radiobutton = Radiobutton(
            self.frame_transaction,
            text="Withdraw",
            variable=self.radio_transaction_type,
            value=1,
        )
        self.radio_deposit: Radiobutton = Radiobutton(
            self.frame_transaction,
            text="Deposit",
            variable=self.radio_transaction_type,
            value=2,
        )
        self.label_transaction_type.pack(side="top", padx=5)
        self.radio_withdraw.pack(side="left")
        self.radio_deposit.pack(side="left")

        self.frame_transaction_amount: Frame = Frame(self.window)
        self.field_transaction_amount: Entry = Entry(self.frame_transaction_amount)
        self.button_transaction_submit: Button = Button(
            self.frame_transaction_amount,
            text="SUBMIT",
            command=self.conduct_transaction,
        )
        self.field_transaction_amount.pack()
        self.button_transaction_submit.pack(anchor="center", pady=10)
