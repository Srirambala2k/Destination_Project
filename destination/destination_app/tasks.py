from celery import shared_task
from django.utils import timezone
from .models import Log

@shared_task
def send_data_to_destination(data, destination_id):
    try:
        # Send data to the destination (implementation depends on how your destinations are set up)
        # You can use requests or any other method to send data
        response = send_to_destination(data, destination_id)

        # Log the event after sending the data
        Log.objects.create(
            account_id=data['account_id'],
            destination_id=destination_id,
            received_data=data,
            status="success",
            received_timestamp=timezone.now(),
            processed_timestamp=timezone.now(),
        )
    except Exception as e:
        # Log the failure
        Log.objects.create(
            account_id=data['account_id'],
            destination_id=destination_id,
            received_data=data,
            status="failed",
            received_timestamp=timezone.now(),
            processed_timestamp=timezone.now(),
        )
        raise e
