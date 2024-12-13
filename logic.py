import csv
from tkinter import Frame, Label
from accounts import Account, SavingAccount
from gui import Gui


class Logic(Gui):
    """
    A class that handles the logic for bank account transactions and GUI interactions.

    Class Attributes:
        __CHECKING (int): Constant representing a checking account type.
        __SAVINGS (int): Constant representing a savings account type.
        __WITHDRAW (int): Constant representing a withdrawal transaction.
        __DEPOSIT (int): Constant representing a deposit transaction.
        USER_ACCOUNT: The currently logged-in user's account.
        ACCOUNT_PIN (str): The PIN for the current account.
    """

    __CHECKING: int = 1
    __SAVINGS: int = 2
    __WITHDRAW: int = 1
    __DEPOSIT: int = 2
    USER_ACCOUNT: Account | SavingAccount
    ACCOUNT_PIN: str = ""

    def setup_gui(self) -> None:
        """
        Set up the GUI and validate user credentials.

        Performs these actions:
        1. Validates first name, last name, and PIN
        2. Checks account credentials against a CSV file
        3. Creates the appropriate account type
        4. Updates GUI

        Raises:
            ValueError: If input validation fails
        """
        first_name: str = self.field_first_name.get()
        last_name: str = self.field_last_name.get()
        pin: str = self.field_pin.get()
        account_type: int = self.radio_account_choice.get()
        account_type_as_word: str = ""
        label_alert: Label = self.label_alert
        label_balance: Label = self.label_balance
        frame_transaction: Frame = self.frame_transaction

        try:
            if not first_name or not first_name.strip().isalpha():
                self.label_balance.pack_forget()
                self.frame_transaction.pack_forget()
                self.frame_transaction_amount.pack_forget()
                raise ValueError("Invalid first name. Name must contain letters.")
            if not last_name or not last_name.strip().isalpha():
                self.label_balance.pack_forget()
                self.frame_transaction.pack_forget()
                self.frame_transaction_amount.pack_forget()
                raise ValueError("Invalid last name. Name must contain letters.")
            if not pin:
                self.label_balance.pack_forget()
                self.frame_transaction.pack_forget()
                self.frame_transaction_amount.pack_forget()
                raise ValueError("Pin is required.")
            if account_type == 0:
                raise ValueError("Account type selection is required.")

            if account_type == Logic.__CHECKING:
                account_type_as_word = "Checking"
            elif account_type == Logic.__SAVINGS:
                account_type_as_word = "Saving"
            else:
                account_type_as_word = ""

            with open("credentials.csv", "r") as file_reader:
                credential_file: csv.reader = csv.reader(file_reader)
                for line in credential_file:
                    if (
                        account_type_as_word == line[0].strip()
                        and first_name.lower().strip() == line[1].lower().strip()
                        and last_name.lower().strip() == line[2].lower().strip()
                        and pin.strip() in line
                    ):
                        Logic.ACCOUNT_PIN = pin
                        first_name = (
                            first_name[:1].upper() + first_name[1:].lower().strip()
                        )
                        last_name = (
                            last_name[:1].upper() + last_name[1:].lower().strip()
                        )
                        label_alert.config(
                            text=f"Welcome {first_name} {last_name}", fg="green"
                        )
                        label_alert.pack()
                        account_balance = float(line[-2])
                        label_balance.config(
                            text=f"Your balance is: {account_balance:.2f}", fg="green"
                        )
                        label_balance.pack()
                        frame_transaction.pack(anchor="center", pady=10)
                        self.frame_transaction_amount.pack(anchor="center")
                        if self.radio_account_choice.get() == Logic.__CHECKING:
                            Logic.USER_ACCOUNT = Account(
                                first_name, last_name, account_balance
                            )
                            return
                        if self.radio_account_choice.get() == Logic.__SAVINGS:
                            Logic.USER_ACCOUNT = SavingAccount(
                                first_name, last_name, account_balance
                            )
                            return
                    else:
                        self.label_balance.pack_forget()
                        self.frame_transaction.pack_forget()
                        self.frame_transaction_amount.pack_forget()
                        label_alert.config(
                            text="First Name/Last Name/Pin was incorrect.", fg="red"
                        )
                        label_alert.pack()

        except ValueError as ve:
            label_alert.config(text=str(ve), fg="red")
            label_alert.pack()

    def conduct_transaction(self) -> None:
        """
        Perform a transaction for the current user account.

        Performs the following actions:
        1. Validates transaction amount and type
        2. Processes withdrawal or deposit based on account type
        3. Updates the credentials file
        4. Updates GUI with result

        Raises:
            ValueError: If transaction validation fails
        """
        transaction_amount: str = self.field_transaction_amount.get()
        account_type: int = self.radio_account_choice.get()
        account_type_as_word: str = ""
        transaction_type: int = self.radio_transaction_type.get()
        is_transaction_successful: bool

        try:
            if transaction_type == 0:
                raise ValueError("Transaction type is required.")
            if (
                transaction_amount == ""
                or transaction_amount is None
                or transaction_amount.isalpha()
            ):
                raise ValueError("Enter a numeric amount to transact.")

            if account_type == Logic.__CHECKING:
                account_type_as_word = "Checking"
            elif account_type == Logic.__SAVINGS:
                account_type_as_word = "Saving"
            else:
                account_type_as_word = ""

            if (
                account_type == Logic.__CHECKING
                and transaction_type == Logic.__WITHDRAW
            ):
                is_transaction_successful, message = Logic.USER_ACCOUNT.withdraw(
                    float(transaction_amount.strip())
                )
            if account_type == Logic.__CHECKING and transaction_type == Logic.__DEPOSIT:
                is_transaction_successful, message = Logic.USER_ACCOUNT.deposit(
                    float(transaction_amount.strip())
                )
            if account_type == Logic.__SAVINGS and transaction_type == Logic.__WITHDRAW:
                is_transaction_successful, message = Logic.USER_ACCOUNT.withdraw(
                    float(transaction_amount.strip())
                )
            if account_type == Logic.__SAVINGS and transaction_type == Logic.__DEPOSIT:
                is_transaction_successful, message = Logic.USER_ACCOUNT.deposit(
                    float(transaction_amount.strip())
                )

            if is_transaction_successful:
                with open("credentials.csv", "r") as file_reader:
                    lines = list(csv.reader(file_reader))

                for i, line in enumerate(lines):
                    if (
                        line[0] == account_type_as_word
                        and line[1].lower() == Logic.USER_ACCOUNT.get_name()[0].lower()
                        and line[2].lower() == Logic.USER_ACCOUNT.get_name()[1].lower()
                    ):
                        account_parts = Logic.USER_ACCOUNT.__str__().split(",")

                        lines[i] = account_parts + [Logic.ACCOUNT_PIN]
                        break

                with open("credentials.csv", "w", newline="") as file_writer:
                    csv.writer(file_writer).writerows(lines)

                self.label_balance.config(
                    text=f"Your balance is: {Logic.USER_ACCOUNT.get_balance():.2f}",
                    fg="green",
                )
                self.label_alert.config(text=message, fg="green")
            else:
                self.label_alert.config(text=message, fg="red")

            self.label_balance.pack()
            self.label_alert.pack()

        except ValueError as ve:
            self.label_alert.config(text=str(ve), fg="red")
            self.label_alert.pack()
