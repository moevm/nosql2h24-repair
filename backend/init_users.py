from dao.user import UserDao
from schemas.user import UserCreateSchema, Role
from utils.password import get_password_hash


async def create_users():
    admin_init = UserCreateSchema(
        name='Иван',
        lastname='Петров',
        middlename='Александрович',
        email='ivan.petrov@example.com',
        password=get_password_hash('admin123'),
        role=Role.admin
    )

    foreman_init = UserCreateSchema(
        name='Мария',
        lastname='Смирнова',
        middlename='Ивановна',
        email='maria.smirnova@example.com',
        password=get_password_hash('securepassword1'),
        role=Role.foreman
    )

    worker_init = UserCreateSchema(
        name='Дмитрий',
        lastname='Кузнецов',
        middlename='Петрович',
        email='dmitry.kuznetsov@example.com',
        password=get_password_hash('securepassword2'),
        role=Role.worker
    )

    customer_init = UserCreateSchema(
        name='Алексей',
        lastname='Сидоров',
        middlename='Леонидович',
        email='alex.sidorov@example.com',
        password=get_password_hash('securepassword3'),
        role=Role.customer
    )

    exist_admin = await UserDao.find_user_by_email(admin_init.email)
    if exist_admin is None:
        await UserDao.create_user(admin_init)
        
    exist_foreman = await UserDao.find_user_by_email(foreman_init.email)
    if exist_foreman is None:
        await UserDao.create_user(foreman_init)
        
    exist_worker = await UserDao.find_user_by_email(worker_init.email)
    if exist_worker is None:
        await UserDao.create_user(worker_init)
        
    exist_customer = await UserDao.find_user_by_email(customer_init.email)
    if exist_customer is None:
        await UserDao.create_user(customer_init)
