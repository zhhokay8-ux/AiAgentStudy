from typing import TypedDict


class UserState(TypedDict):
    name: str
    age:int

user_state : UserState = {
    "name" : "alice",
    "age" : 18
}

print(user_state)
print(user_state["age"])