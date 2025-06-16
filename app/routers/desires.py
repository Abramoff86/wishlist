from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.auth import get_current_user


from app.backend.db_depends import get_db
from app.schemas import CreateDesire
from app.models.desires import Desire
from app.models.user import User


router = APIRouter(prefix='/desires', tags=['desires'])


@router.get("/{willing_id}")
async def get_all_desires(db: Annotated[AsyncSession, Depends(get_db)], willing_id: int):
    willing = await db.scalar(select(User).where(User.id == willing_id, User.is_active == True))
    if willing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    desires = await db.scalars(select(Desire).where(Desire.willing_id == willing_id, Desire.is_active == True, Desire.reservation == False))
    return desires.all()


@router.get("/reservation/{willing_id}")
async def get_all_reservation_desires(db: Annotated[AsyncSession, Depends(get_db)], willing_id: int):
    willing = await db.scalar(select(User).where(User.id == willing_id, User.is_active == True))
    if willing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    desires = await db.scalars(select(Desire).where(Desire.willing_id == willing_id, Desire.reservation == True, Desire.is_active == True))
    return desires.all()


@router.post("/")
async def create_desire(db: Annotated[AsyncSession, Depends(get_db)], create_desire: CreateDesire, get_user: Annotated[dict, Depends(get_current_user)]):
    await db.execute(insert(Desire).values(name=create_desire.name,
                                            link=create_desire.link,
                                            price=create_desire.price,
                                            willing_id=get_user.get('id')))
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }



@router.delete("/{desires_id}")
async def delete_desires(db: Annotated[AsyncSession, Depends(get_db)], desires_id: int, get_user: Annotated[dict, Depends(get_current_user)]):
    desire = await db.scalar(select(Desire).where(Desire.id == desires_id, Desire.willing_id == get_user.get('id')))
    if desire is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no desire found'
        )
    desire.is_active = False
    await db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Desire delete is successful'
    }


@router.put('/detail/{desires_id}')
async def desires_reservation(db: Annotated[AsyncSession, Depends(get_db)], desires_id: int):
    desires_reservation = await db.scalar(select(Desire).where(Desire.id == desires_id, Desire.is_active == True, Desire.reservation == False))
    if desires_reservation:
        desires_reservation.name = desires_reservation.name
        desires_reservation.link = desires_reservation.link
        desires_reservation.price = desires_reservation.price
        desires_reservation.reservation = True

        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Desires update is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='There is no desires found'
        )

@router.put('/unbook/{desires_id}')
async def desires_unbook(db: Annotated[AsyncSession, Depends(get_db)], desires_id: int, get_user: Annotated[dict, Depends(get_current_user)]):
    desires_unbook = await db.scalar(select(Desire).where(Desire.id == desires_id, Desire.is_active == True, Desire.reservation == True))
    if desires_unbook.willing_id != get_user.get('id'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You have not enough permission for this action'
        )
    if desires_unbook:
        desires_unbook.name = desires_unbook.name
        desires_unbook.link = desires_unbook.link
        desires_unbook.price = desires_unbook.price
        desires_unbook.reservation = False

        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Desires update is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='There is no desires found'
        )




