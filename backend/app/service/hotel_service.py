from app.config.database_config import db_dependency
from app.config.logging_config import get_logger
from app.repository.hotel_repository import hotel_repository
from app.util.calculate_rate import calculate_effective_rate
from app.model.generic_response import GenericResponse
from app.exception.base_exception import BaseAppException

logger = get_logger(class_name=__name__)

class HotelService:

    @classmethod
    def get_all_hotels(cls, db: db_dependency):
        try:
            logger.info("Fetching all hotels")
            hotels = hotel_repository.get_all_hotels(db=db)
            return GenericResponse.success(
                message="Hotels fetched successfully",
                results=hotels,
                status_code=200
            )
        except BaseAppException as e:
            logger.info(f"Get all hotels failed: {e.message}")
            return GenericResponse.failed(
                message=f"Get all hotels failed: {e.message}",
                results={},
                status_code=e.status
            )
        except Exception as e:
            logger.error(f"Unexpected error fetching hotels: {str(e)}")
            return GenericResponse.failed(
                message="Unable to fetch hotels",
                results={},
                status_code=500
            )

    @classmethod
    def get_hotel(cls, db: db_dependency, hotel_id: int):
        try:
            logger.info(f"Fetching hotel with ID: {hotel_id}")
            hotel = hotel_repository.get_hotel_by_id(db=db, hotel_id=hotel_id)
            if not hotel:
                return GenericResponse.failed(
                    message="Hotel not found",
                    results={},
                    status_code=404
                )

            hotel_dict = {
                "id": hotel.id,
                "name": hotel.name,
                "location": hotel.location,
                "description": hotel.description,
                "created_at": hotel.created_at,
                "room_types": []
            }

            for room_type in hotel.room_types:
                effective_rate = calculate_effective_rate(room_type=room_type, db=db)
                hotel_dict["room_types"].append({
                    "id": room_type.id,
                    "hotel_id": room_type.hotel_id,
                    "name": room_type.name,
                    "description": room_type.description,
                    "base_rate": room_type.base_rate,
                    "created_at": room_type.created_at,
                    "effective_rate": effective_rate
                })

            return GenericResponse.success(
                message="Hotel fetched successfully",
                results=hotel_dict,
                status_code=200
            )

        except BaseAppException as e:
            logger.info(f"Get hotel failed: {e.message}")
            return GenericResponse.failed(
                message=f"Get hotel failed: {e.message}",
                results={},
                status_code=e.status
            )
        except Exception as e:
            logger.error(f"Unexpected error fetching hotel: {str(e)}")
            return GenericResponse.failed(
                message="Unable to fetch hotel",
                results={},
                status_code=500
            )

    @classmethod
    def create_hotel(cls, db: db_dependency, hotel_data: dict):
        try:
            logger.info("Creating new hotel")
            db_hotel = hotel_repository.create_hotel(db=db, hotel_data=hotel_data)
            return GenericResponse.success(
                message="Hotel created successfully",
                results=db_hotel,
                status_code=201
            )
        except BaseAppException as e:
            logger.info(f"Create hotel failed: {e.message}")
            return GenericResponse.failed(
                message=f"Create hotel failed: {e.message}",
                results={},
                status_code=e.status
            )
        except Exception as e:
            logger.error(f"Unexpected error creating hotel: {str(e)}")
            return GenericResponse.failed(
                message="Unable to create hotel",
                results={},
                status_code=500
            )

    @classmethod
    def update_hotel(cls, db: db_dependency, hotel_id: int, update_data: dict):
        try:
            logger.info(f"Updating hotel with ID: {hotel_id}")
            db_hotel = hotel_repository.get_hotel_by_id(db=db, hotel_id=hotel_id)
            if not db_hotel:
                return GenericResponse.failed(
                    message="Hotel not found",
                    results={},
                    status_code=404
                )
            updated_hotel = hotel_repository.update_hotel(db=db, db_hotel=db_hotel, update_data=update_data)
            return GenericResponse.success(
                message="Hotel updated successfully",
                results=updated_hotel,
                status_code=200
            )
        except BaseAppException as e:
            logger.info(f"Update hotel failed: {e.message}")
            return GenericResponse.failed(
                message=f"Update hotel failed: {e.message}",
                results={},
                status_code=e.status
            )
        except Exception as e:
            logger.error(f"Unexpected error updating hotel: {str(e)}")
            return GenericResponse.failed(
                message="Unable to update hotel",
                results={},
                status_code=500
            )

    @classmethod
    def delete_hotel(cls, db: db_dependency, hotel_id: int):
        try:
            logger.info(f"Deleting hotel with ID: {hotel_id}")
            db_hotel = hotel_repository.get_hotel_by_id(db=db, hotel_id=hotel_id)
            if not db_hotel:
                return GenericResponse.failed(
                    message="Hotel not found",
                    results={},
                    status_code=404
                )
            hotel_repository.delete_hotel(db=db, db_hotel=db_hotel)
            return GenericResponse.success(
                message="Hotel deleted successfully",
                results={},
                status_code=204
            )
        except BaseAppException as e:
            logger.info(f"Delete hotel failed: {e.message}")
            return GenericResponse.failed(
                message=f"Delete hotel failed: {e.message}",
                results={},
                status_code=e.status
            )
        except Exception as e:
            logger.error(f"Unexpected error deleting hotel: {str(e)}")
            return GenericResponse.failed(
                message="Unable to delete hotel",
                results={},
                status_code=500
            )
