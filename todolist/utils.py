def update_from_kv(instance, kv: dict):
    for k, v in kv.items():
        setattr(instance, k, v)
    instance.save()
    return instance
