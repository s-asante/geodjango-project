import factory
from factory.django import DjangoModelFactory
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from locations.models import Location


class UserFactory(DjangoModelFactory):
    
    
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            self.set_password(extracted)
        else:
            self.set_password('defaultpass123')


class AdminUserFactory(UserFactory):
    
    
    is_staff = True
    is_superuser = True


class LocationFactory(DjangoModelFactory):
    
    
    class Meta:
        model = Location
    
    name = factory.Faker('company')
    description = factory.Faker('text', max_nb_chars=200)
    address = factory.Faker('address')
    point = factory.LazyFunction(
        lambda: Point(
            factory.Faker('longitude').generate(),
            factory.Faker('latitude').generate(),
            srid=4326
        )
    )


class NYCLocationFactory(LocationFactory):
    
    
    point = factory.LazyFunction(
        lambda: Point(
            factory.Faker('pyfloat', min_value=-74.1, max_value=-73.9).generate(),
            factory.Faker('pyfloat', min_value=40.6, max_value=40.9).generate(),
            srid=4326
        )
    )
    address = factory.Faker('street_address', locale='en_US')