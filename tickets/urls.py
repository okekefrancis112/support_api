from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('ticket_list/', views.TicketView.as_view(), name='ticket_list'),
    path('api/new_ticket/', views.NewTicket.as_view(), name='new_ticket'),
    path('api/tickets/<int:ticket_pk>/', views.TicketDetail.as_view(), name='get_ticket_detail'),
    path('api/tickets/<int:ticket_pk>/reply/', views.ReplyTicket.as_view(), name='reply_ticket'),
    path('api/tickets/<int:ticket_pk>/replies/', views.GetReply.as_view(), name='get_replies'),
    path('api/replies/<int:reply_pk>/', views.DeleteReply.as_view(), name='delete_reply'),
    path('<int:year>/<str:month>/tickets_pdf', views.TicketDownloadView.as_view(), name="tickets_pdf" ),
]