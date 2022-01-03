import random







def unique_otp_generator(instance):

    key = random.randint(1, 999999)
    print(key)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_otp_generator(instance)
    return key

