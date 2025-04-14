from datetime import datetime, timedelta, time
from factory import Faker, post_generation, SubFactory
from factory.django import DjangoModelFactory

from bookings.models import Booking
from tests.factories.doctor_factory import DoctorFactory
from tests.factories.user_factory import UserFactory


class BookingFactory(DjangoModelFactory):
    class Meta:
        model = Booking

    patient = SubFactory(UserFactory)
    doctor = SubFactory(DoctorFactory)
    appointment_date = Faker('date_between', start_date='today', end_date='+30d')
    appointment_time = Faker('time_object')
    status = Faker('random_element', elements=['pending', 'confirmed', 'completed', 'cancelled', 'no_show'])

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Get the doctor and time from kwargs
        doctor = kwargs.get('doctor')
        appointment_date = kwargs.get('appointment_date')
        appointment_time = kwargs.get('appointment_time')
        
        # Maximum time to try (8 PM)
        max_time = time(20, 0)
        original_time = appointment_time

        # If there's already a booking at this time, adjust the time
        while Booking.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists():
            # Add 30 minutes to the time
            current_time = datetime.combine(datetime.today(), appointment_time)
            new_time = current_time + timedelta(minutes=30)
            appointment_time = new_time.time()

            # If we've gone past max_time, start from original time on next day
            if appointment_time > max_time:
                appointment_date += timedelta(days=1)
                appointment_time = original_time

            # Update kwargs with new time
            kwargs['appointment_time'] = appointment_time
            kwargs['appointment_date'] = appointment_date

        return super()._create(model_class, *args, **kwargs)
    
    @post_generation
    def ensure_unique_booking(self, create, extracted, **kwargs):
        """Ensure no double bookings for same doctor at same time"""
        if not create:
            return
