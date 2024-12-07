from bson import ObjectId
from database import db
from schemas.project import ProjectCreate, Project, Procurement, Stage, Risk, ProcurementResponse, RiskResponse, \
    StageResponse
from schemas.user import UserDao, Contact, ContactResponse
from schemas.utils import object_id_to_str, generate_id


async def create_project(project_crate: ProjectCreate, user: UserDao) -> Project:
    project_collection = db.get_collection('project')
    contact = Contact(
        username=f'{user.lastname} {user.name} {user.middlename}',
        role=user.role
    )
    project_crate.add_contact(user.id, contact)
    result = await project_collection.insert_one(project_crate.model_dump())
    return await get_project_by_id(result.inserted_id)


async def get_project_by_id(project_id: str) -> Project | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one({'_id': ObjectId(project_id)})
    if project is None:
        return None
    project = object_id_to_str(project)
    return Project(**project)


async def get_project_by_name(project_name: str) -> Project | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one({'name': project_name})
    if project is None:
        return None
    project = object_id_to_str(project)
    return Project(**project)


async def get_projects_by_user(user_id: str) -> list[Project] | None:
    project_collection = db.get_collection('project')
    cursor = project_collection.find(
        {f"contacts.{user_id}": {"$exists": True}}
    )
    projects_list = await cursor.to_list()
    result = []
    for project in projects_list:
        project = object_id_to_str(project)
        result.append(Project(**project))
    return result


async def add_contact_to_project(project_id: str, user: UserDao) -> Project | None:
    project_collection = db.get_collection('project')
    result = await project_collection.update_one(
        {"_id": ObjectId(project_id)},
        {
            "$set": {
                f"contacts.{user.id}": {
                    "username": f"{user.lastname} {user.name} {user.middlename}",
                    "role": user.role,
                }
            }
        },
    )
    return await get_project_by_id(project_id)


async def get_contacts_by_project_id(project_id: str) -> list[ContactResponse] | list[None] | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one({"_id": ObjectId(project_id)}, {"contacts": 1})
    if project and "contacts" in project:
        contacts = [ContactResponse(id=contact_id, **contact_data) for contact_id, contact_data in
                    project["contacts"].items()]
        return contacts
    elif project is None:
        return None
    return []


async def get_contact_by_id(project_id: str, contact_id: str) -> ContactResponse | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one({"_id": ObjectId(project_id)})
    if not project:
        return None

    contact = project.get("contacts", {}).get(contact_id)
    if not contact or contact.get("user_id") != ObjectId(contact_id):
        return None
    return ContactResponse(**contact)


async def add_procurement_to_project(project_id: str, procurement_create: Procurement) -> Project | None:
    project_collection = db.get_collection('project')
    procurement = procurement_create.model_dump()
    procurement['quantity'] = str(procurement['quantity'])
    procurement['price'] = str(procurement['price'])
    result = await project_collection.update_one(
        {"_id": ObjectId(project_id)},
        {
            "$set": {f"procurements.{generate_id()}": procurement}
        }
    )
    return await get_project_by_id(project_id)


async def get_procurements_by_project_id(project_id: str) -> list[ProcurementResponse] | list[None] | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one({"_id": ObjectId(project_id)}, {"procurements": 1})
    if project and "procurements" in project:
        procurements = [ProcurementResponse(id=procurement_id, **procurement_data) for procurement_id, procurement_data
                        in
                        project["procurements"].items()]
        return procurements
    elif project is None:
        return None
    return []


async def get_procurement_by_id(project_id: str, procurement_id: str) -> ProcurementResponse | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one(
        {
            "_id": ObjectId(project_id),
            f"procurements.{procurement_id}": {"$exists": True}
        },
        {
            f"procurements.{procurement_id}": 1
        }
    )

    if project:
        procurement = project["procurements"][procurement_id]
        return ProcurementResponse(id=procurement_id, **procurement)
    return None


async def add_stage_to_project(project_id: str, stage_create: Stage):
    project_collection = db.get_collection('project')
    result = await project_collection.update_one(
        {'_id': ObjectId(project_id)},
        {
            "$set": {f"stages.{generate_id()}": stage_create.model_dump()}
        }
    )
    return await get_project_by_id(project_id)


async def get_stages_by_project_id(project_id: str) -> list[StageResponse] | list[None] | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one({"_id": ObjectId(project_id)}, {"stages": 1})
    if project and "stages" in project:
        stages = [StageResponse(id=stage_id, **stage_data) for stage_id, stage_data in
                  project["stages"].items()]
        return stages
    elif project is None:
        return None
    return []


async def get_stage_by_id(project_id: str, stage_id: str) -> StageResponse | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one(
        {
            "_id": ObjectId(project_id),
            f"stages.{stage_id}": {"$exists": True}
        },
        {
            f"stages.{stage_id}": 1
        }
    )

    if project:
        stage = project["stages"][stage_id]
        return StageResponse(id=stage_id, **stage)
    return None


async def add_risk_to_project(project_id: str, risk_create: Risk):
    project_collection = db.get_collection('project')
    result = await project_collection.update_one(
        {"_id": ObjectId(project_id)},
        {
            "$set": {f"risks.{generate_id()}": risk_create.model_dump()}
        }
    )
    return await get_project_by_id(project_id)


async def get_risks_by_project_id(project_id: str) -> list[RiskResponse] | list[None] | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one({"_id": ObjectId(project_id)}, {"risks": 1})
    if project and "risks" in project:
        risks = [RiskResponse(id=risk_id, **risk_data) for risk_id, risk_data in
                 project["risks"].items()]
        return risks
    elif project is None:
        return None
    return []



async def get_risk_by_id(project_id: str, risk_id: str) -> RiskResponse | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one(
        {
            "_id": ObjectId(project_id),
            f"risks.{risk_id}": {"$exists": True}
        },
        {
            f"risks.{risk_id}": 1
        }
    )

    if project:
        stage = project["risks"][risk_id]
        return RiskResponse(id=risk_id, **stage)
    return None
