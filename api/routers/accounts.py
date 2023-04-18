# router.py
from fastapi import (
    Depends,
    HTTPException,
    status,
    Response,
    APIRouter,
    Request,
)
from jwtdown_fastapi.authentication import Token
from queries.authenticator import authenticator

from pydantic import BaseModel

from queries.accounts import (
    AccountIn,
    AccountOut,
    AccountQueries,
    DuplicateAccountError,
    AccountOutWithPassword
)
from queries.authenticator import authenticator

class AccountForm(BaseModel):
    username: str
    password: str

class AccountToken(Token):
    account: AccountOut

class HttpError(BaseModel):
    detail: str

router = APIRouter()


@router.post("/api/accounts", response_model=AccountToken | HttpError)
async def create_account(
    info: AccountIn,
    request: Request,
    response: Response,
    accounts: AccountQueries = Depends(),
):
    hashed_password = authenticator.hash_password(info.password)
    try:
        account = accounts.create(info, hashed_password)
    except DuplicateAccountError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create an account with those credentials",
        )
    form = AccountForm(username=info.username, password=info.password)
    token = await authenticator.login(response, request, form, accounts)
    return AccountToken(account=account, **token.dict())

@router.get("/token", response_model=AccountOut | HttpError)
async def get_account(
    repo: AccountQueries = Depends(),
    curr_account: dict=Depends(authenticator.get_current_account_data)
) -> AccountOut:
    return curr_account


# @router.get("/api/outfits", response_model = AllOutfits)
# def list_outfits(
#     repo: OutfitRepo = Depends()
#     # curr_account: dict=Depends(authenticator.get_current_account_data)
# ) -> AllOutfits:
#     outfits = repo.list_outfits()
#     return outfits
