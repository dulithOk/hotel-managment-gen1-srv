from app.config.config import settings

def validate_config_vars():
    # Get all attributes of the settings object
    config_vars = {name: getattr(settings, name) for name in settings.__fields__}
    
    # Find missing (None) variables
    missing_vars = [name for name, value in config_vars.items() if value is None]
    
    if missing_vars:
        raise ValueError(f"Missing required configuration variables: {', '.join(missing_vars)}")
