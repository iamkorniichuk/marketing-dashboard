def get_all_fieldnames(model_class):
    results = []
    for field in model_class._meta.get_fields():
        if not field.auto_created:
            results.append(field.name)
    return results
