from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, status

from dao.stat import StatDao
from schemas.stat import StatSchema
from utils.role import get_admin_role, get_customer_role
from utils.token import get_current_user

router = APIRouter()


@router.post("/get_stat")
async def get_stat(stat_data: StatSchema, user = Depends(get_customer_role)):
    result = 0
    try:
        result = await StatDao.get_stats(stat_data.project_ids, stat_data.stat_type.value,
                                         stat_data.start_date, stat_data.end_date)
    except InvalidId as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Некорректные id проектов'
        )
    
    return result