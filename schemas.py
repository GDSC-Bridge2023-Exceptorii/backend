from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str
    disabled: bool


class UserCreate(UserBase):
    password: str



class User(UserBase):
    id: int
    email: str | None = None
    full_name: str | None = None
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True

class UserInDB(UserBase):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class Tutorial(BaseModel):
    id: int
    title: str
    description: str | None = None
    owner_id: int

    class Config:
        orm_mode = True

class TutorialBase(BaseModel):
    title: str
    description: str | None = None

class TutorialCreate(TutorialBase):
    pass

class Summarization(BaseModel):
    id: int
    title: str
    description: str | None = None
    owner_id: int

    class Config:
        orm_mode = True

    

class SummarizationBase(BaseModel):
    title: str
    description: str | None = None

class SummarizationCreate(SummarizationBase):
    pass
