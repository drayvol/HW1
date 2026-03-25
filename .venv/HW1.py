#Домашнее задания №1
import abc
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from enum import Enum

class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'

class TransactionType(Enum):
    CHARGE = 'charge'
    TOP_UP = 'top_up'

class TaskStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

class User:
    def __init__(self, email: str,password:str, user_id:int, balance: int = 0) -> None:
        self.__email = email
        self.__password = password
        self.__balance = balance
        self.__user_id = user_id
        self.__creation_date = datetime.now()
        self._role= Role.USER
    @property
    def user_id(self) ->int:
        return self.__user_id
    @property
    def email(self) -> str:
        return self.__email
    @property
    def balance(self) -> int:
        return self.__balance
    @property
    def role(self) -> Role:
        return self._role
    def top_up(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.__balance += amount
    def charge(self, amount: int) -> None:
        if amount > self.__balance:
            raise ValueError("Недостаточно средств на балансе")
        self.__balance -= amount
    def __repr__(self) -> str:
        return f"<User name={self.__email} user_id  = {self.__user_id} balance={self.__balance}>"
class Admin(User):
    def __init__(self, email: str, password:str, user_id:int) -> None:
        super().__init__(email,password,user_id)
        self._role = Role.ADMIN
        self.__permissions:list[str]=["read", "write", "delete"]
    @property
    def permissions(self) -> list[str]:
        return list(self.__permissions)
class MLModel(abc.ABC):
    def __init__(self, model:str,model_id:int,price:int, description:str) -> None:
        self.__model = model
        self.__model_id = model_id
        self.__price = price
        self.__description = description
    @property
    def price(self) -> int:
        return self.__price
    @property
    def description(self) -> str:
        return self.__description
    @abc.abstractmethod
    def recognise (self, task: 'Task')->'Result':
        pass
class OCR(MLModel):
    def recognise(self, task: 'Task')->'Result':
        task.complete()
        return Result(task=task, model=self, output='OCR')

class Task:
    def __init__(self,task_id:int, name:str, user:User, model: MLModel, input_data:Any) -> None:
        self.__task_id = task_id
        self.__name = name
        self.__user = user
        self.__model = model
        self.__input_data = input_data
        self.__task_status = TaskStatus.PENDING
        self.__creation_date = datetime.now()
    @property
    def task_id(self) -> int:
        return self.__task_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def model(self) -> MLModel:
        return self.__model

    @property
    def user(self) -> User:
        return self.__user

    @property
    def input_data(self) -> Any:
        return self.__input_data

    @property
    def task_status(self) -> TaskStatus:
        return self.__task_status

    @property
    def creation_date(self) -> datetime:
        return self.__creation_date

    def complete(self) -> None:
        self.__task_status=TaskStatus.COMPLETED
    def failed(self) -> None:
        self.__task_status = TaskStatus.FAILED
    def run(self)-> 'Result':
        return self.__model.recognise(self)
    def __repr__(self) -> str:
        return f"<Task name={self.__name} task_id  = {self.__task_id} status={self.__task_status}>"

@dataclass
class Transaction:
    transaction_type: TransactionType
    amount: int
    user: User
    task: Optional['Task'] = None
    created_at: datetime=field(default_factory=datetime.now)

@dataclass
class Result:
    task: Task
    model: MLModel
    output: str
    created_at: datetime = field(default_factory=datetime.now)

class History:
    def __init__(self):
        self.__storage: list[Result] = []
    def append(self, result: Result) -> None:
        self.__storage.append(result)
    def get_all(self) -> list[Result]:
        return self.__storage
    def clear(self)->None:
        self.__storage.clear()


class MLService:
    def __init__(self) -> None:
        self.__history: History = History()
        self.__transactions: list[Transaction] = []

    def top_up(self, user: User, amount: int) -> None:
        try:
            user.top_up(amount)
            self.__transactions.append(Transaction(
                transaction_type=TransactionType.TOP_UP,
                amount=amount,
                user=user,
            ))
        except ValueError as e:
            print(f"[MLService] Ошибка пополнения: {e}")
            raise

    def process(self, task: Task) -> Result:
        user = task.user
        try:
            user.charge(task.model.price)
            result = task.run()
            self.__history.append(result)
            self.__transactions.append(Transaction(
                transaction_type=TransactionType.CHARGE,
                amount=task.model.price,
                user=user,
                task=task,
            ))
            return result
        except ValueError as e:
            task.failed()
            print(f"[MLService] Ошибка обработки: {e}")
            raise

    def get_history(self) -> list[Result]:
        return self.__history.get_all()

    def get_transactions(self) -> list[Transaction]:
        return list(self.__transactions)

    def clear_history(self) -> None:
        self.__history.clear()

