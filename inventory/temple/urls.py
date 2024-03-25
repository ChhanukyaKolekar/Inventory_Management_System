from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('update_items/',views.add_items,name='update'),
    path('irumudi_recepit/',views.irumudi_book,name='irumudi_book'),
    path('irumudi_items/',views.items_list,name='items_list'),
    path('maaladharane_receipt/',views.maaladharane,name='maaladharane'),
    path('ghee_coconut_receipt/',views.ghee,name='ghee'),
    path('irumudi_record/',views.irumudi_register,name='irumudi_register'),
    path('cash_report/',views.expenses,name='expenses'),
    path('temple_seva/', views.temple_seva_ ,name='temple_s'),
    # path('irumudi_record/irumudi_record/', views.record_tabel ,name='records_page'),
    path('pdf/',views.generate_pdf,name="gen_pdf")


]
