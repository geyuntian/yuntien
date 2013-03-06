#get query object, with or without filters
def build_query(cls, filters=None):
    query = cls.objects.all()
    
    if filters is not None:
        for filter in filters:
            query = filter(query)

    return query
