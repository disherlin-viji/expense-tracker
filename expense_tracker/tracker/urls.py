from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_transaction, name='add'),
    path('edit/<int:id>/', views.edit_transaction, name='edit'),
    path('delete/<int:id>/', views.delete_transaction, name='delete'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('transactions/',views.transactions_page,name='transactions_page'),
    path('categories/',views.categories,name='categories'),
    path('change-username/',views.change_username,name='change_username'),
    path('change-password/',views.change_password,name='change_password'),
    path('delete-account/',views.delete_account,name='delete_account'),
]