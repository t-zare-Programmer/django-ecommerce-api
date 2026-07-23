import factory
from factory import Faker
from apps.accounts.models import CustomUser


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        skip_postgeneration_save = True

    mobile_number = factory.Sequence(
        lambda n: f"0912000{n:04d}"
    )

    email = factory.LazyAttribute(
        lambda obj: f"user{obj.mobile_number}@test.com"
    )

    name = Faker("first_name")
    family = Faker("last_name")

    gender = "True"

    is_active = True

    is_admin = False

    password = factory.PostGenerationMethodCall(
        "set_password",
        "12345678",
    )