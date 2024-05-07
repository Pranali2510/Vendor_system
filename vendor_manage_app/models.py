from django.db import models
import pandas as pd, datetime
from django.db.models import Avg, F
from django.dispatch import receiver
from django.db.models.signals import post_save

class Vendor(models.Model):
    vendor_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(blank=True, null=True)
    quality_rating_avg = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfillment_rate = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'vendor'
        unique_together = (('id', 'vendor_code'),)
    
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey('Vendor', models.DO_NOTHING, db_column='vendor', to_field='vendor_code', blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    on_time_delivery_rate = models.FloatField(blank=True, null=True)
    quality_rating_avg = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfillment_rate = models.FloatField(blank=True, null=True)
    class Meta:
        db_table = 'historical_performance'

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey('Vendor', models.DO_NOTHING, db_column='vendor', to_field='vendor_code')
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=30)
    quality_rating = models.FloatField(blank=True, null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(blank=True, null=True)
    po_deliverd_date =  models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'purchase_order'
        unique_together = (('id', 'po_number'),)

@receiver(post_save, sender=PurchaseOrder)
def vendor_performance_evaluate(sender, instance, **kwargs):
    pos_issue = PurchaseOrder.objects.filter(vendor=instance.vendor).all()
    total_pos_issue = pos_issue.count()
    completed_pos = pd.DataFrame(list(PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed').values('delivery_date','po_deliverd_date','quality_rating','acknowledgment_date')))
    if (instance.status).lower() == 'completed':
        # Calculate the On-Time Delivery Rate for the vendor
        total_complete_pos = len(completed_pos)
        if total_complete_pos > 0:
            ontime_pos = completed_pos.loc[completed_pos['delivery_date'] >= completed_pos['po_deliverd_date']]
            ontime_delivery_rate = len(ontime_pos) / total_complete_pos
            if total_pos_issue > 0:
                fulfillment_rate = total_complete_pos/total_pos_issue
            else:
                fulfillment_rate = 0.0
            instance.vendor.fulfillment_rate = fulfillment_rate
            if instance.quality_rating is not None:
                quality_rating_df = completed_pos[completed_pos['quality_rating'].notna()]
                count_quality_rating = len(quality_rating_df)
                if count_quality_rating > 0:
                    # Calculate the sum of the 'quality_rating' column
                    total_quality_rates = quality_rating_df['quality_rating'].sum()
                    quality_rating_avg = total_quality_rates / count_quality_rating
                    instance.vendor.quality_rating_avg = quality_rating_avg
        else:
            ontime_delivery_rate = 0.0
        instance.vendor.on_time_delivery_rate = ontime_delivery_rate
        instance.vendor.save()
    
    if instance.acknowledgment_date is not None:
        acknowledge_pos = PurchaseOrder.objects.filter(vendor=instance.vendor, acknowledgment_date__isnull=False, issue_date__isnull = False)
        count_acknowledge_pos = len(acknowledge_pos)
        if count_acknowledge_pos > 0:
            average_response_time = acknowledge_pos.aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response_time']
            days = average_response_time.days
            seconds = average_response_time.seconds
            microseconds = average_response_time.microseconds
            td = datetime.timedelta(days=days,seconds=seconds, microseconds=microseconds)
            # Calculate total seconds
            total_seconds = td.total_seconds()
            # Convert total_seconds to float
            average_response_time_float = total_seconds / (24 * 60 * 60)
            instance.vendor.average_response_time = average_response_time_float
            instance.vendor.save()