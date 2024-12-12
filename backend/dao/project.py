from datetime import datetime
from bson import ObjectId

from dao.base import BaseDao
from database import db
from schemas.project import ProjectCreate, ProjectResponse, Procurement, ProjectStatus, Stage, Risk, ProcurementResponse, \
    RiskResponse, \
    StageResponse, ProjectUpdate, RiskUpdate, ProcurementUpdate, StageUpdate
from schemas.user import User, Contact, ContactResponse
from schemas.utils import object_id_to_str, generate_id, get_date_now


class ProjectDao(BaseDao):
    collection = db.get_collection('project')

    @classmethod
    async def create_project(cls, project_create: ProjectCreate, user: User) -> ProjectResponse | None:
        contact = Contact(
            username=f'{user.lastname} {user.name} {user.middlename}',
            role=user.role
        )
        project_create.add_contact(user.id, contact)
        created_id = await cls._create(project_create.model_dump())
        return await cls.get_project_by_id(created_id)

    @classmethod
    async def delete_project(cls, project_id: str) -> str:
        return await cls._delete_by_id(project_id)

    @classmethod
    async def get_project_by_id(cls, project_id: str) -> ProjectResponse | None:
        project = await cls._get_one_by_id(project_id)
        if project is None:
            return None
        return ProjectResponse(**project)

    @classmethod
    async def update_project_by_id(cls, project_id: str, project_update: ProjectUpdate) -> ProjectResponse | None:
        update_data = project_update.model_dump()
        updated_id = await cls._update(project_id, update_data)
        return await cls.get_project_by_id(updated_id)

    @classmethod
    async def get_project_by_name(cls, project_name: str) -> ProjectResponse | None:
        project = await cls._get_one_by_field('name', project_name)
        if project is None:
            return None
        return ProjectResponse(**project)

    @classmethod
    async def get_all_projects(cls, project_name: str = "", project_status: ProjectStatus = ProjectStatus.none_status, 
                               start_date: datetime = None, end_date: datetime = None, user_id: str = "") -> list[ProjectResponse] | list[None]:
        
        filters = {}

        if project_name:
            filters["name"] = {"$regex": project_name, "$options": "i"}
        if project_status:
            filters["status"] = str(project_status.value)
        if start_date:
            filters["start_date"] = {"$gte": start_date}
        if end_date:
            filters["end_date"] = {"$lte": end_date}
        if user_id:
            filters[f"contacts.{user_id}"] = {"$exists": True}
        
        print(filters)
        cursor = cls.collection.find(filters)
        projects_list = await cursor.to_list()
        result = []
        for project in projects_list:
            project = object_id_to_str(project)
            result.append(ProjectResponse(**project))
        return result

    @classmethod
    async def add_contact_to_project(cls, project_id: str, user: User) -> ProjectResponse | None:
        updated_id = await cls._update_with_query(
            {"_id": ObjectId(project_id)},
            {
                "$set": {
                    f"contacts.{user.id}": {
                        "username": f"{user.lastname} {user.name} {user.middlename}",
                        "role": user.role,
                        "updated_at": get_date_now(),
                        "created_at": user.created_at
                    }
                }
            }
        )
        return await cls.get_project_by_id(updated_id)

    @classmethod
    async def get_contacts_by_project_id(cls, project_id: str) -> list[ContactResponse] | list[None] | None:
        project = await cls.collection.find_one({"_id": ObjectId(project_id)}, {"contacts": 1})
        if project and "contacts" in project:
            contacts = [ContactResponse(id=contact_id, **contact_data) for contact_id, contact_data in
                        project["contacts"].items()]
            return contacts
        elif project is None:
            return None
        return []

    @classmethod
    async def get_contact_by_id(cls, project_id: str, contact_id: str) -> ContactResponse | None:
        project = await cls._get_one_by_id(project_id)
        if not project:
            return None

        contact = project.get("contacts", {}).get(contact_id)
        if not contact or contact.get("user_id") != ObjectId(contact_id):
            return None
        return ContactResponse(**contact)

    @classmethod
    async def delete_contact(cls, project_id, contact_id: str) -> ProjectResponse | None:
        project = await cls._get_one_by_id(project_id)
        
        if not project:
            return None

        contacts = project.get("contacts", {})
        if contact_id in contacts:
            del contacts[contact_id]
        else:
            return None

        stages = project.get("stages", {})
    
        for stage_id, stage in stages.items():
            tasks = stage.get("tasks", {})
            for task_id, task in tasks.items():
                workers = task.get("workers", {})
                if contact_id in workers:
                    del workers[contact_id]
    
        update_result = await cls.collection.replace_one(
            {"_id": ObjectId(project_id)},
            project
        )
        
        if update_result.modified_count == 0:
            return None
    
        return await cls.get_project_by_id(project_id)

    @classmethod
    async def add_procurement_to_project(cls, project_id: str,
                                         procurement_create: Procurement) -> ProjectResponse | None:
        procurement = procurement_create.model_dump()
        procurement['quantity'] = str(procurement['quantity'])
        procurement['price'] = str(procurement['price'])
        result = await cls.collection.update_one(
            {"_id": ObjectId(project_id)},
            {
                "$set": {f"procurements.{generate_id()}": procurement}
            }
        )
        return await cls.get_project_by_id(project_id)

    @classmethod
    async def delete_procurement(cls, project_id: str, procurement_id: str) -> str | None:
        return await cls._update_with_query(
            {
                "_id": ObjectId(project_id),
                f"procurements.{procurement_id}": {"$exists": True}
            },
            {
                "$unset": {f"procurements.{procurement_id}": ""}
            }
        )

    @classmethod
    async def get_procurements_by_project_id(cls, project_id: str) -> list[ProcurementResponse] | list[None] | None:
        project = await cls.collection.find_one({"_id": ObjectId(project_id)}, {"procurements": 1})
        if project and "procurements" in project:
            procurements = [ProcurementResponse(id=procurement_id, **procurement_data) for
                            procurement_id, procurement_data
                            in
                            project["procurements"].items()]
            return procurements
        elif project is None:
            return None
        return []

    @classmethod
    async def get_procurement_by_id(cls, project_id: str, procurement_id: str) -> ProcurementResponse | None:
        project = await cls.collection.find_one(
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

    @classmethod
    async def update_procurement_by_id(cls, project_id: str, procurement_id: str,
                                       procurement_update: ProcurementUpdate) -> ProcurementResponse | None:

        update_data = procurement_update.model_dump()

        updated_id = await cls._update_with_query(
            {
                "_id": ObjectId(project_id),
                f"procurements.{procurement_id}": {"$exists": True}
            },
            {
                "$set": {
                    f"procurements.{procurement_id}.item_name": update_data["item_name"],
                    f"procurements.{procurement_id}.quantity": update_data["quantity"],
                    f"procurements.{procurement_id}.price": update_data["price"],
                    f"procurements.{procurement_id}.inStock": update_data["inStock"],
                    f"procurements.{procurement_id}.units": update_data["units"],
                    f"procurements.{procurement_id}.delivery_date": update_data["delivery_date"],
                    f"procurements.{procurement_id}.created_by": update_data["created_by"],
                    f"procurements.{procurement_id}.updated_at": get_date_now(),
                }
            }
        )

        return await cls.get_procurement_by_id(updated_id, procurement_id)

    @classmethod
    async def add_stage_to_project(cls, project_id: str, stage_create: Stage):
        updated_id = await cls._update_with_query(
            {'_id': ObjectId(project_id)},
            {
                "$set": {f"stages.{generate_id()}": stage_create.model_dump()}
            }
        )
        return await cls.get_project_by_id(updated_id)

    @classmethod
    async def delete_stage(cls, project_id: str, stage_id: str) -> str | None:
        updated_id = await cls._update_with_query(
            {
                "_id": ObjectId(project_id),
                f"stages.{stage_id}": {"$exists": True}
            },
            {
                "$unset": {f"stages.{stage_id}": ""}
            }
        )

        return stage_id

    @classmethod
    async def get_stages_by_project_id(cls, project_id: str) -> list[StageResponse] | list[None] | None:
        project = await cls.collection.find_one({"_id": ObjectId(project_id)}, {"stages": 1})
        if project and "stages" in project:
            stages = [StageResponse(id=stage_id, **stage_data) for stage_id, stage_data in
                      project["stages"].items()]
            return stages
        elif project is None:
            return None
        return []

    @classmethod
    async def get_stage_by_id(cls, project_id: str, stage_id: str) -> StageResponse | None:
        project = await cls.collection.find_one(
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

    @classmethod
    async def update_stage_by_id(cls, project_id: str, stage_id: str,
                                 stage_update: StageUpdate) -> StageResponse | None:
        update_data = stage_update.model_dump()
        update_data["updated_at"] = get_date_now()
        updated_id = await cls._update_with_query(
            {
                "_id": ObjectId(project_id),
                f"stages.{stage_id}": {"$exists": True}
            },
            {
                "$set": {
                    f"stages.{stage_id}.name": update_data["name"],
                    f"stages.{stage_id}.start_date": update_data["start_date"],
                    f"stages.{stage_id}.end_date": update_data["end_date"],
                    f"stages.{stage_id}.updated_at": update_data["updated_at"],
                }
            }
        )
        return await cls.get_stage_by_id(updated_id, stage_id)

    @classmethod
    async def add_risk_to_project(cls, project_id: str, risk_create: Risk):
        updated_id = await cls._update_with_query(
            {"_id": ObjectId(project_id)},
            {
                "$set": {f"risks.{generate_id()}": risk_create.model_dump()}
            }
        )
        return await cls.get_project_by_id(updated_id)

    @classmethod
    async def delete_risk(cls, project_id: str, risk_id: str) -> str | None:
        updated_id = await cls._update_with_query(
            {
                "_id": ObjectId(project_id),
                f"risks.{risk_id}": {"$exists": True}
            },
            {
                "$unset": {f"risks.{risk_id}": ""}
            }
        )
        return risk_id

    @classmethod
    async def get_risks_by_project_id(cls, project_id: str) -> list[RiskResponse] | list[None] | None:
        project = await cls.collection.find_one({"_id": ObjectId(project_id)}, {"risks": 1})
        if project and "risks" in project:
            risks = [RiskResponse(id=risk_id, **risk_data) for risk_id, risk_data in
                     project["risks"].items()]
            return risks
        elif project is None:
            return None
        return []

    @classmethod
    async def get_risk_by_id(cls, project_id: str, risk_id: str) -> RiskResponse | None:
        project = await cls.collection.find_one(
            {
                "_id": ObjectId(project_id),
                f"risks.{risk_id}": {"$exists": True}
            },
            {
                f"risks.{risk_id}": 1
            }
        )

        if project:
            risk = project["risks"][risk_id]
            return RiskResponse(id=risk_id, **risk)
        return None

    @classmethod
    async def update_risk_by_id(cls, project_id: str, risk_id: str, risk_update: RiskUpdate) -> RiskResponse | None:
        update_data = risk_update.model_dump()
        update_data["updated_at"] = get_date_now()

        result = await cls.collection.update_one(
            {
                "_id": ObjectId(project_id),
                f"risks.{risk_id}": {"$exists": True}
            },
            {
                "$set": {
                    f"risks.{risk_id}.name": update_data["name"],
                    f"risks.{risk_id}.description": update_data["description"],
                    f"risks.{risk_id}.updated_at": update_data["updated_at"]
                }
            }
        )

        if result.modified_count == 0:
            return None

        return await cls.get_risk_by_id(project_id, risk_id)
