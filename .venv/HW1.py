    #Домашнее задания №1
import abc
    from dataclasses import dataclass
    from datetime import datetime
    from typing import Any

    class User:
        def __init__(self, name: str, user_id:int, balance: int = 0) -> None:
            self.__name = name
            self.__balance = balance
            self.__user_id = user_id
            self.__creation_date = datetime.now()
        @property
        def user_id(self) ->int:
            return self.__user_id
        @property
        def name(self) -> str:
            return self.__name
        @property
        def balance(self) -> int:
            return self.__balance
        def top_up(self, amount: int) -> None:
            self.__balance += amount
        def charge(self, amount: int) -> None:
            if amount > self.__balance:
                raise ValueError("Недостаточно средств на балансе")
            self.__balance -= amount
        def __repr__(self) -> str:
            return f"<User name={self.__name} user_id  = {self.__user_id} balance={self.__balance}>"
    class Task:

        def __init__(self,task_id:int, name:str, user:User, input_data:Any) -> None:
            self.__task_id = task_id
            self.__name = name
            self.__user = user
            self.__input_data = input_data
            self.__task_status = 'pending'
            self.__creation_date = datetime.now()
        @property
        def task_id(self) -> int:
            return self.__task_id

        @property
        def name(self) -> str:
            return self.__name

        @property
        def user(self) -> User:
            return self.__user

        @property
        def input_data(self) -> Any:
            return self.__input_data

        @property
        def task_status(self) -> str:
            return self.__task_status

        @property
        def creation_date(self) -> datetime:
            return self.__creation_date

        def complete(self) -> None:
            self.__task_status = 'completed'
        def failed(self) -> None:
            self.__task_status = 'failed'
        def __repr__(self) -> str:
            return f"<Task name={self.__name} task_id  = {self.__task_id} status={self.__task_status}>"

    class MLModel(abc.ABC):
        def __init__(self, model:str):
            self.__model = model
        @abc.abstractmethod
        def recognise (self, task: Task)->'Result':
            pass

    @dataclass
    class Result:
        task: Task
        model: MLModel
        output: str

    class OCR(MLModel):
        def recognise(self, task: Task)->Result:
            task.complete()
            return Result(task=task, model=self, output='ORC')

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
        def __init__(self, model:MLModel):
            self.__model = model
            self.__history = History()
        def get_history(self)->list[Result]:
            return self.__history.get_all()
        def process(self, task: Task)->Result:
            result= self.__model.recognise(task=task)
            self.__history.append(result)
            return result
        def clear_history(self)->None:
            self.__history.clear()

