from datetime import time
from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory

from doctors.models import (
    Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday,
    TimeRange
)
from tests.factories.doctor_factory import DoctorFactory


class TimeRangeFactory(DjangoModelFactory):
    class Meta:
        model = TimeRange

    start = Faker('time_object')
    end = Faker('time_object')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Ensure end time is after start time
        if kwargs.get('start') >= kwargs.get('end'):
            kwargs['end'] = time(
                (kwargs['start'].hour + 1) % 24,
                kwargs['start'].minute
            )
        return super()._create(model_class, *args, **kwargs)


class ScheduleFactory:
    """Factory for creating doctor schedules for all days of the week"""
    
    @classmethod
    def create_schedule(cls, doctor=None, num_slots_per_day=3):
        """
        Create a complete schedule for a doctor with specified number of time slots per day
        
        Args:
            doctor: Doctor instance to create schedule for
            num_slots_per_day: Number of time slots to create for each day
            
        Returns:
            dict: Dictionary containing all created schedule objects
        """
        if doctor is None:
            doctor = DoctorFactory()

        schedule = {}
        day_models = {
            'sunday': Sunday,
            'monday': Monday,
            'tuesday': Tuesday,
            'wednesday': Wednesday,
            'thursday': Thursday,
            'friday': Friday,
            'saturday': Saturday
        }

        for day_name, day_model in day_models.items():
            # Create the day schedule
            day_schedule = day_model.objects.create(user=doctor)
            
            # Create time ranges for this day
            time_ranges = []
            for _ in range(num_slots_per_day):
                time_range = TimeRangeFactory()
                day_schedule.time_range.add(time_range)
                time_ranges.append(time_range)
            
            schedule[day_name] = {
                'day': day_schedule,
                'time_ranges': time_ranges
            }

        return schedule
