def sina(request, dash, *args, **kwargs):
    print(kwargs)
    print(args)
    return request


sina(54, "sina", 2, kwargs={"sina": "mame", "prisa": 2})
