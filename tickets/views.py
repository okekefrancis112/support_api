
from django.shortcuts import render,get_object_or_404
from .models import Ticket, Reply
from rest_framework import status
from rest_framework.views import APIView
from . import serializers
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime
import calendar 
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter 
# from drf_yasg.utils import swagger_auto_schema


User = get_user_model()

# Create your views here.

class TicketView(APIView):
    serializer_class=serializers.TicketSerializer
    permission_classes = [IsAuthenticated]
    
    # @swagger_auto_schema(operation_summary="Get all Orders")
    def get(self,request):
        if request.user.is_staff:
            tickets=Ticket.objects.all().order_by('-updated_at')
        else:
            tickets=Ticket.objects.filter(owner=request.user).order_by('-updated_at')
            
        serializer=self.serializer_class(tickets, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class NewTicket(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class=serializers.TicketSerializer

    def post(self, request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            user = request.user
            if user.is_staff:
                res = {
                    "error": "You are not allowed to create a ticket. "
                }
                return Response(data=res, status=status.HTTP_403_FORBIDDEN_REQUEST)
            description = serializer.data['description']
            subject = serializer.data['subject']
            ticket = Ticket.objects.create(subject=subject, description=description, owner=user)
            res = {
                "id": ticket.id,
                "subject": ticket.subject,
            }
            return Response(data=res, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketDetail(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class=serializers.TicketSerializer

    def get(self, request, ticket_pk):
        ticket = get_object_or_404(Ticket, pk=ticket_pk)
        serializer = self.serializer_class(instance=ticket)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def put(self,request,ticket_id):
        
        ticket=get_object_or_404(Ticket,pk=ticket_id)
        
        serializer=self.serializer_class(instance=ticket,data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data,status=status.HTTP_200_OK)

        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ReplyTicket(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class=serializers.ReplySerializer

    def post(self, request, ticket_pk):
        ticket = get_object_or_404(Ticket, pk=ticket_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            comment = serializer.data['comment']
            reply = Reply.objects.create(comment=comment, ticket=ticket, owner=user)
            ticket.updated_at = timezone.now()
            ticket.save()
            res = {
                "id": reply.id,
                "status": "Success",
            }
            return Response(data=res, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetReply(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class=serializers.ReplySerializer

    def get(self, request, ticket_pk):
        ticket = get_object_or_404(Ticket, pk=ticket_pk)
        replies = ticket.replies.get_queryset().order_by('created_at')
        serializer = self.serializer_class(instance=replies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteReply(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class=serializers.ReplySerializer

    def delete(self, request, reply_pk):
        reply = get_object_or_404(Reply, pk=reply_pk)
        if reply.owner == request.user:
            reply.delete()
            return Response(data="Reply deleted", status=status.HTTP_204_NO_CONTENT)
        res = {
            "error": "You are not allowed to delete to this reply. "
        }
        return Response(data=res, status=status.HTTP_403_FORBIDDEN)
    
class TicketDownloadView(APIView):
    serializer_class=serializers.TicketSerializer
    permission_classes = [IsAdminUser]
    
    # @swagger_auto_schema(operation_summary="Get all Orders")
    def get(self,request, year=datetime.now().year, month=datetime.now().strftime('%B')):
        month = month.capitalize()
        
        month_number = list(calendar.month_name).index(month)
        month_number = int(month_number)
        tickets = Ticket.objects.filter(
            created_at__year = year, 
            created_at__month = month_number
        )
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
        textob = c.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 14)
        lines = [
            "This is line 1",
            "This is line 2",
            "This is line 3",
        ]
        
        for line in lines:
            textob.textLine(line)
            
        for ticket in tickets:
            lines.append(ticket.owner)
            lines.append(ticket.ticket_id)
            lines.append(ticket.ticket_name)
            lines.append(ticket.ticket_type)
            lines.append(ticket.ticket_status)
            lines.append(ticket.ticket_description)
            lines.append(ticket.created_at)
            lines.append(ticket.updated_at)
            lines.append("========================================================")
            
        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)
        
        return FileResponse(buf, as_attachment=True, filename="tickets.pdf")
        # serializer=self.serializer_class(tickets, many=True)

        # return Response(data=serializer.data, status=status.HTTP_200_OK)

