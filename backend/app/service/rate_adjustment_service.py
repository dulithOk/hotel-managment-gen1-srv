from app.config.database_config import db_dependency
from app.config.logging_config import get_logger
from app.repository.rate_adjustment_repository import rate_adjustment_repository
from app.repository.room_type_repository import room_type_repository
from app.model.generic_response import GenericResponse
from app.exception.base_exception import BaseAppException

logger = get_logger(class_name=__name__)

class RateAdjustmentService:

    @classmethod
    def get_rate_adjustments(cls, db: db_dependency, room_type_id: int):
        try:
            logger.info(f"Fetching rate adjustments for room_type_id={room_type_id}")
            
            room_type = room_type_repository.get_by_id(db=db, room_type_id=room_type_id)
            if not room_type:
                return GenericResponse.failed(message="Room type not found", results={}, status_code=404)
            
            adjustments = rate_adjustment_repository.get_by_room_type(
                db=db,
                room_type_id=room_type_id
            )

            return GenericResponse.success(
                message="Rate adjustments fetched successfully",
                results=adjustments,
                status_code=200
            )

        except BaseAppException as e:
            logger.info(f"Get rate adjustments failed: {e.message}")
            return GenericResponse.failed(
                message=f"Get rate adjustments failed: {e.message}",
                results={},
                status_code=e.status
            )
        except Exception as e:
            logger.error(f"Unexpected error fetching rate adjustments: {str(e)}")
            return GenericResponse.failed(
                message="Unable to fetch rate adjustments",
                results={},
                status_code=500
            )

    @classmethod
    def create_rate_adjustment(cls, db: db_dependency, adjustment_data: dict):
        try:
            logger.info("Creating rate adjustment")
            room_type = room_type_repository.get_by_id(
                db=db,
                room_type_id=adjustment_data.get("room_type_id")
            )

            if not room_type:
                return GenericResponse.failed(
                    message="Room type not found",
                    results={},
                    status_code=404
                )

            adjustment = rate_adjustment_repository.create(
                db=db,
                adjustment_data=adjustment_data
            )

            return GenericResponse.success(
                message="Rate adjustment created successfully",
                results=adjustment,
                status_code=201
            )

        except BaseAppException as e:
            logger.info(f"Create rate adjustment failed: {e.message}")
            return GenericResponse.failed(
                message=f"Create rate adjustment failed: {e.message}",
                results={},
                status_code=e.status
            )
        except Exception as e:
            logger.error(f"Unexpected error creating rate adjustment: {str(e)}")
            return GenericResponse.failed(
                message="Unable to create rate adjustment",
                results={},
                status_code=500
            )
