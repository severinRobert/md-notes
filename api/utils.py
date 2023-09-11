# Desc: Utility functions for API

def model_to_dict(model, exclude: list[str] = []):
    """Convert SQLAlchemy model to dictionary."""
    # extract model SQLAlchemy class into dictionary
    model = model.__dict__
    # remove SQLAlchemy internal variables
    model.pop('_sa_instance_state')
    # remove excluded variables
    for key in exclude:
        model.pop(key)

    return model