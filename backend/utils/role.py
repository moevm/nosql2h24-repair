from fastapi import Depends, HTTPException, status

from schemas.user import User, Role
from utils.token import get_current_user


def get_admin_role(user: User = Depends(get_current_user)):
    if user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Нет прав администратора'
        )
    return user


def get_foreman_role(user: User = Depends(get_current_user)):
    if user.role != Role.foreman and user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Нет прав прораба'
        )
    return user


def get_customer_role(user: User = Depends(get_current_user)):
    if user.role != Role.customer and user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Нет прав заказчика'
        )
    return user
