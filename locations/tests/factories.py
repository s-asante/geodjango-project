import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from locations.models import Location

fake = Faker()


class UserFactory(DjangoModelFactory):
    
    
    class Meta:
        model = User
        skip_postgeneration_save = True  
    
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
    
    
    class Meta:
        model = User
        skip_postgeneration_save = True  
    
    is_staff = True
    is_superuser = True


class LocationFactory(DjangoModelFactory):
    
    
    class Meta:
        model = Location
    
    name = factory.Faker('company')
    description = factory.Faker('text', max_nb_chars=200)
    address = factory.Faker('address')
    
    @factory.lazy_attribute
    def point(self):
        
        lon = fake.longitude()
        lat = fake.latitude()
        return Point(float(lon), float(lat), srid=4326)


class NYCLocationFactory(LocationFactory):
    
    
    @factory.lazy_attribute
    def point(self):
        
        lon = fake.pyfloat(min_value=-74.1, max_value=-73.9)
        lat = fake.pyfloat(min_value=40.6, max_value=40.9)
        return Point(lon, lat, srid=4326)
    
    address = factory.Faker('street_address')