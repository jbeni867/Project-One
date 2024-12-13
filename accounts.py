from typing import Tuple

# Author: Jordy Benitez
# Assignment: Lab 9


class Account:
    """
    A class representing a basic bank checking account.
    """

    def __init__(self, first_name: str, last_name: str, balance: float = 0) -> None:
        """
        Initialize a new Account instance.

        Args:
            first_name (str): The first name of the account holder.
            last_name (str): The last name of the account holder.
            balance (float): Initial account balance. Defaults to 0.
        """
        self.__account_first_name = first_name
        self.__account_last_name = last_name
        self.__account_balance = balance
        self.set_balance(balance)

    def deposit(self, amount: float) -> Tuple[bool, str]:
        """
        Deposit money into the account.

        Args:
            amount (float): The amount to deposit.

        Returns:
            Tuple[bool, str]: A tuple containing a bool and a message.
        """
        if amount <= 0:
            return False, "Deposit amount must be greater than zero."
        else:
            self.set_balance(self.get_balance() + amount)
            return True, f"Successfully deposited ${amount:.2f}"

    def withdraw(self, amount: float) -> Tuple[bool, str]:
        """
        Withdraw money from the account.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            Tuple[bool, str]: A tuple containing a bool and a message.
        """
        if amount <= 0:
            return False, "Withdrawal amount must be greater than zero."
        elif amount > self.get_balance():
            return False, "Insufficient funds for withdrawal."

        self.set_balance(self.get_balance() - amount)
        return True, f"Successfully withdrew ${amount:.2f}"

    def get_balance(self) -> float:
        """
        Get the current account balance.

        Returns:
            float: The current account balance.
        """
        return self.__account_balance

    def get_name(self) -> Tuple[str, str]:
        """
        Get the account holder's first and last name.

        Returns:
            Tuple[str, str]: A tuple containing the first and last name.
        """
        return self.__account_first_name, self.__account_last_name

    def set_balance(self, value: float) -> None:
        """
        Set the account balance, making sure it's not negative.

        Args:
            value (float): The balance to set.
        """
        if value < 0:
            self.__account_balance = 0
        else:
            self.__account_balance = value

    def set_name(self, value: str) -> None:
        """
        Set the account holder's first name.

        Args:
            value (str): The first name to set.
        """
        self.__account_first_name = value

    def __str__(self) -> str:
        """
        Get a string of the account.

        Returns:
            str: A comma-separated string with account details.
        """
        return f"Checking,{self.__account_first_name},{self.__account_last_name},{self.get_balance():.2f}"


class SavingAccount(Account):
    """
    A class representing a savings account with interest and minimum balance rules.

    Class Attributes:
        MINIMUM (float): The minimum required balance for a savings account.
        RATE (float): The interest rate applied to the account.
    """

    MINIMUM: float = 100
    RATE: float = 0.02

    def __init__(self, first_name: str, last_name: str, balance: float = None) -> None:
        """
        Initialize a new SavingAccount instance.

        Args:
            first_name (str): The first name of the account holder.
            last_name (str): The last name of the account holder.
            balance (float): Initial account balance. Defaults to MINIMUM.
        """
        if balance is None:
            balance = SavingAccount.MINIMUM

        balance = max(balance, SavingAccount.MINIMUM)

        super().__init__(first_name, last_name, balance)
        self.__deposit_count = 0

    def apply_interest(self) -> None:
        """
        Apply interest to the account balance based on the RATE.
        """
        self.set_balance(self.get_balance() + (self.get_balance() * SavingAccount.RATE))

    def deposit(self, amount: float) -> Tuple[bool, str]:
        """
        Deposit money into the savings account, applying interest every 5 deposits.

        Args:
            amount (float): The amount to deposit.

        Returns:
            Tuple[bool, str]: A tuple containing a bool and a message.
        """
        if amount <= 0:
            return False, "Deposit amount must be greater than zero."

        is_successful = super().deposit(amount)[0]
        if is_successful:
            self.__deposit_count += 1
            if self.__deposit_count % 5 == 0 and self.__deposit_count != 0:
                self.apply_interest()

        return is_successful, f"Successfully deposited ${amount:.2f}"

    def withdraw(self, amount: float) -> Tuple[bool, str]:
        """
        Withdraw money from the savings account, ensuring minimum balance is maintained.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            Tuple[bool, str]: A tuple containing a bool and a message.
        """
        if amount <= 0:
            return False, "Withdrawal amount must be greater than zero."
        elif self.get_balance() - amount < SavingAccount.MINIMUM:
            return (
                False,
                f"Cannot withdraw. Balance must remain above ${SavingAccount.MINIMUM}",
            )

        self.set_balance(self.get_balance() - amount)
        return True, f"Successfully withdrew ${amount:.2f}"

    def set_balance(self, value: float) -> None:
        """
        Set the account balance, ensuring it's not below the minimum required balance.

        Args:
            value (float): The balance to set.
        """
        if value < SavingAccount.MINIMUM:
            super().set_balance(SavingAccount.MINIMUM)
        else:
            super().set_balance(value)

    def __str__(self) -> str:
        """
        Get a string of the account.

        Returns:
            str: A comma-separated string with account details.
        """
        first_name, last_name = self.get_name()
        return f"Saving,{first_name},{last_name},{self.get_balance():.2f}"
