from django.db.models.signals import post_save
from django.dispatch import receiver
from Inicio_sesion.models import Company, CustomUser
from Formulario.models import Form

@receiver(post_save, sender=Company)
def update_related_models(sender, instance, **kwargs):
    # Update related CustomUser instances
    related_users = CustomUser.objects.filter(company=instance)
    for user in related_users:
        user.companyName = instance.companyName  # Assuming you want to update some related field
        user.save()

    # Update related Form instances
    related_forms = Form.objects.filter(company=instance)
    for form in related_forms:
        form.companyName = instance.companyName  # Assuming you want to update some related field
        form.save()
