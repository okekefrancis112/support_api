from email.policy import default
from rest_framework import serializers
from tickets.models import Ticket, Reply

class TicketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    owner = serializers.CharField(read_only=True)
    ticket_id = serializers.CharField(max_length=255, allow_blank=False)
    ticket_name = serializers.CharField(max_length=250)
    ticket_type = serializers.CharField(default="LOW PRIORITY")
    ticket_status = serializers.CharField(default="OPEN")
    ticket_description =serializers.CharField()
    human_time = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Ticket
        
    
    def get_human_time(self, obj):
        time = ''
        if isinstance(obj, Ticket):
            return obj.get_date()
        return time
    
    
class ReplySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    replied_by = serializers.CharField(source='owner.email', read_only=True)
    is_customer_service = serializers.CharField(source='owner.is_staff', read_only=True)
    comment = serializers.CharField(allow_blank=True)
    human_time = serializers.SerializerMethodField(read_only=True)

    def get_human_time(self, obj):
        time = ''
        if isinstance(obj, Reply):
            return obj.get_date()
        return time


        