def update_from_payload(instance, payload):
    for k, v in payload.dict().items():
        setattr(instance, k, v)
    instance.save()
    return instance
