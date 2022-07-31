from typing import List

from sqlalchemy.orm import Session

from app.schemes import Message
from app.services.pet.logic import PetLogic
from app.services.pet.models import Pet
from app.services.store import schemes
from app.services.store.logic import StoreLogic
from app.services.store.models import Store
from core import auth
from core.cache.backend import RedisBackend
from core.cache.cache import CacheManager
from core.cache.key_marker import CustomKeyMaker
from core.db.sessions import get_db
from core.exceptions.pet import PetDoesNotFound
from core.exceptions.store import OrderAlreadyExists, OrderDoesNotFound
from fastapi import APIRouter, Depends, HTTPException, status

cache_manager = CacheManager(backend=RedisBackend(), key_maker=CustomKeyMaker())
router = APIRouter()
logic = StoreLogic(model=Store)
pet_logic = PetLogic(model=Pet)
auth_handler = auth.AuthHandler()


@router.get(
    "/store/store_list",
    tags=["store"],
    name="Get list of all orders",
    status_code=status.HTTP_200_OK,
    response_model=List[schemes.Order],
)
@cache_manager.cached(prefix="get_order_list")
async def get_list(
    db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)
):
    orders = await logic.get_all(session=db)
    lst_ = []
    if not orders:
        return lst_
    for order in orders:
        lst_.append(order.__dict__)
    return lst_


@router.get(
    "/order/inventory",
    tags=["store"],
    name="Returns pet inventories by status",
    status_code=status.HTTP_200_OK,
)
async def find_by_id(
    db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)
):
    res = await logic.get_inventory(db=db)
    return res


@router.post(
    "/store",
    tags=["store"],
    name="Place an order for pet",
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": Message},
        404: {"model": Message},
    },
)
async def create_pet(
    order: schemes.Order,
    db: Session = Depends(get_db),
    user=Depends(auth_handler.auth_wrapper),
):
    o = await logic.get_by_id(id=order.id, session=db)
    if o:
        raise HTTPException(
            detail=OrderAlreadyExists.message, status_code=OrderAlreadyExists.error_code
        )

    pet = await pet_logic.get_by_id(id=order.pet_id, session=db)
    if not pet:
        raise HTTPException(
            detail=PetDoesNotFound.message, status_code=PetDoesNotFound.error_code
        )

    res = await logic.create_order(order=order, db=db)
    return res


@router.delete(
    "/store/{order_id}",
    tags=["store"],
    name="Delete Order by id",
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": Message},
    },
)
async def delete_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(auth_handler.auth_wrapper),
):
    order = await logic.get_by_id(id=order_id, session=db)
    if not order:
        raise HTTPException(
            detail=OrderDoesNotFound.message, status_code=OrderDoesNotFound.error_code
        )
    await logic.delete_by_id(id=order_id, session=db)


@router.get(
    "/store/{order_id}",
    tags=["store"],
    name="Finds Order by id",
    response_model=schemes.Order,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": Message},
    },
)
async def find_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(auth_handler.auth_wrapper),
):
    order = await logic.get_by_id(session=db, id=order_id)
    if not order:
        raise HTTPException(
            detail=OrderDoesNotFound.message, status_code=OrderDoesNotFound.error_code
        )
    return order.__dict__
