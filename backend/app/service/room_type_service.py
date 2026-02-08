from app.config.database_config import db_dependency
from app.repository.room_type_repository import room_type_repository
from app.model.generic_response import GenericResponse
from app.util.calculate_rate import calculate_effective_rate
from app.config.logging_config import get_logger
from app.exception.base_exception import BaseAppException
from app.repository.hotel_repository import hotel_repository

logger = get_logger(class_name=__name__)

class RoomTypeService:

    @classmethod
    def get_all_room_types(cls, db: db_dependency, hotel_id: int = None):
        try:
            logger.info("Fetching room types")
            room_types = room_type_repository.get_all(db=db, hotel_id=hotel_id)
            result = []
            for room_type in room_types:
                effective_rate = calculate_effective_rate(room_type=room_type, db=db)
                result.append({
                    "id": room_type.id,
                    "hotel_id": room_type.hotel_id,
                    "name": room_type.name,
                    "description": room_type.description,
                    "base_rate": room_type.base_rate,
                    "created_at": room_type.created_at,
                    "effective_rate": effective_rate
                })
            return GenericResponse.success(message="Room types fetched successfully", results=result, status_code=200)
        
        except BaseAppException as e:
            logger.info(f"Get room type failed: {e.message}")
            return GenericResponse.failed(
                message=f"Get room type failed: {e.message}",
                results={},
                status_code=e.status
            )
            
        except Exception as e:
            logger.error(f"Error fetching room types: {str(e)}")
            return GenericResponse.failed(message="Unable to fetch room types", results={}, status_code=500)

    @classmethod
    def get_room_type(cls, db: db_dependency, room_type_id: int):
        try:
            logger.info(f"Fetching room type {room_type_id}")
            room_type = room_type_repository.get_by_id(db=db, room_type_id=room_type_id)
            if not room_type:
                return GenericResponse.failed(message="Room type not found", results={}, status_code=404)
            
            effective_rate = calculate_effective_rate(room_type=room_type, db=db)
            room_type_dict = {
                "id": room_type.id,
                "hotel_id": room_type.hotel_id,
                "name": room_type.name,
                "description": room_type.description,
                "base_rate": room_type.base_rate,
                "created_at": room_type.created_at,
                "effective_rate": effective_rate
            }
            return GenericResponse.success(message="Room type fetched successfully", results=room_type_dict, status_code=200)
        
        except BaseAppException as e:
            logger.info(f"Fetch room type failed: {e.message}")
            return GenericResponse.failed(
                message=f"Fetch room type failed: {e.message}",
                results={},
                status_code=e.status
            )
            
        except Exception as e:
            logger.error(f"Error fetching room type: {str(e)}")
            return GenericResponse.failed(message="Unable to fetch room type", results={}, status_code=500)

    @classmethod
    def create_room_type(cls, db: db_dependency, room_type_data: dict):
        try:
            hotel = hotel_repository.get_hotel_by_id(db=db, hotel_id=room_type_data.get("hotel_id"))
            if not hotel:
                return GenericResponse.failed(message="Hotel not found", results={}, status_code=404)

            db_room_type = room_type_repository.create(db=db, room_type_data=room_type_data)
            effective_rate = calculate_effective_rate(room_type=db_room_type, db=db)
            result = {
                "id": db_room_type.id,
                "hotel_id": db_room_type.hotel_id,
                "name": db_room_type.name,
                "description": db_room_type.description,
                "base_rate": db_room_type.base_rate,
                "created_at": db_room_type.created_at,
                "effective_rate": effective_rate
            }
            return GenericResponse.success(message="Room type created successfully", results=result, status_code=201)
        
        except BaseAppException as e:
            logger.info(f"Create Room type failed: {e.message}")
            return GenericResponse.failed(
                message=f"Create Room type failed: {e.message}",
                results={},
                status_code=e.status
            )
            
        except Exception as e:
            logger.error(f"Error creating room type: {str(e)}")
            return GenericResponse.failed(message="Unable to create room type", results={}, status_code=500)

    @classmethod
    def update_room_type(cls, db: db_dependency, room_type_id: int, update_data: dict):
        try:
            logger.info(f"Updating room type {room_type_id}")
            db_room_type = room_type_repository.get_by_id(db, room_type_id)
            if not db_room_type:
                return GenericResponse.failed(message="Room type not found", results={}, status_code=404)
            
            updated = room_type_repository.update(db, db_room_type, update_data)
            effective_rate = calculate_effective_rate(updated, db)
            result = {
                "id": updated.id,
                "hotel_id": updated.hotel_id,
                "name": updated.name,
                "description": updated.description,
                "base_rate": updated.base_rate,
                "created_at": updated.created_at,
                "effective_rate": effective_rate
            }
            return GenericResponse.success(message="Room type updated successfully", results=result, status_code=200)
        
        except BaseAppException as e:
            logger.info(f"Update room type failed: {e.message}")
            return GenericResponse.failed(
                message=f"Update room type failed: {e.message}",
                results={},
                status_code=e.status
            )
            
        except Exception as e:
            logger.error(f"Error updating room type: {str(e)}")
            return GenericResponse.failed(message="Unable to update room type", results={}, status_code=500)

    @classmethod
    def delete_room_type(cls, db: db_dependency, room_type_id: int):
        try:
            logger.info(f"Deleting room type {room_type_id}")
            db_room_type = room_type_repository.get_by_id(db=db, room_type_id=room_type_id)
            if not db_room_type:
                return GenericResponse.failed(message="Room type not found", results={}, status_code=404)
            
            room_type_repository.delete(db=db, db_room_type=db_room_type)
            return GenericResponse.success(message="Room type deleted successfully", results={}, status_code=204)
        
        except BaseAppException as e:
            logger.info(f"Delete room type failed: {e.message}")
            return GenericResponse.failed(
                message=f"Delete room type failed: {e.message}",
                results={},
                status_code=e.status
            )
            
        except Exception as e:
            logger.error(f"Error deleting room type: {str(e)}")
            return GenericResponse.failed(message="Unable to delete room type", results={}, status_code=500)
