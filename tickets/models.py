# from re import T
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.contrib.humanize.templatetags import humanize
from django.utils.text import Truncator



User=get_user_model()

def generate_ticket_id():
    # generate unique ticket id
    return str(uuid.uuid4()).split("-")[-1]

# Create your models here.

STATUSES = (
    ('OPEN', 'open'),
    ('CLOSE', 'close'),
    ('IN PROGRESS', 'In Progress'),
    ('PENDING', 'pending'),
)

TYPES = (
    ('HIGH PRIORITY', 'high priority'),
    ('LOW PRIORITY', 'low priority'),
    ('INFORMATION', 'information'),
)

    
class Ticket(models.Model):
    owner = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    ticket_id = models.CharField(max_length=255, blank=True)
    ticket_name = models.CharField(max_length=250)
    ticket_type = models.CharField(choices=TYPES, max_length=100, default="LOW PRIORITY")
    ticket_status = models.CharField(choices=STATUSES, max_length=100, default="OPEN")
    ticket_description = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        # ordering = ('-updated_at')BBBilllBB
        
    def __str__(self):
        return '{} -- {}'.format(self.ticket_name, self.ticket_id)
    
    def save(self, *args, **kwargs):
        if len(self.ticket_id.strip(" ")) == 0:
            self.ticket_id = generate_ticket_id()
        super(Ticket, self).save(*args, **kwargs)
    
class Reply(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    # active = models.BooleanField(default=True)   
    
    # class Meta:
    #     ordering = ('-date_added',)
    
    def __str__(self):
        comment = Truncator(self.comment)
        return comment.chars(30)
    
    def get_date(self):
        return humanize.naturaltime(self.created_at)
    