import pytest
from app.calculations import add, subtract, multiply, division, BankAccount, InsufficientFunds



@pytest.fixture
def zero_bank_account():
    print("Creating empty bank account.")
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (10, 4, 14),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print('testing add fuynction')
    assert add(num1, num2) == expected


def test_subtract():
    result = subtract(5, 3)
    assert result == 2


def test_bank_initial_amount(bank_account):
    # bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    # bank_account = BankAccount()
    assert zero_bank_account.balance == 0

def test_bank_withdraw(bank_account):
    # bank_ac = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_bank_deposit(bank_account):
    # bank_ac = BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_interest(bank_account):
    # bank_ac = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55


@pytest.mark.parametrize("deposited, withdraw, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),
])
def test_bank_transaction(zero_bank_account, deposited, withdraw, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


@pytest.mark.parametrize("deposited, withdraw", [
    (10, 50)
])
def test_insufficient_funds(zero_bank_account, deposited, withdraw):
    with pytest.raises(Exception):
        zero_bank_account.deposit(deposited)
        zero_bank_account.withdraw(withdraw)
