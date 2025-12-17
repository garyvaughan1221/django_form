from decimal import Decimal
import django.db.models as models
# from djangoform.api import model_manager as mgr
import django_mongodb_backend.fields


## meta: Copyright © 2022 by the Association of Statisticians of American Religious Bodies (ASARB)


## NATIONAL MODEL
class National(models.Model):
    id = django_mongodb_backend.fields.ObjectIdAutoField(primary_key=True, editable=False)

    GroupCode = models.CharField(max_length=5) ##mixed type issue
    Congregations = models.IntegerField()
    Adherents = models.IntegerField()
    Adherents_percent_of_Total_Adherents = models.DecimalField(max_digits=5, decimal_places=2)
    Adherents_percent_of_Population = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "National"
        verbose_name_plural = "National"
        db_table = "national"


## BY STATE MODEL
class State(models.Model):
    id = django_mongodb_backend.fields.ObjectIdAutoField(primary_key=True, editable=False)

    StateCode = models.CharField(max_length=3)
    GroupCode = models.CharField(max_length=5) ##mixed type issue
    GroupName = models.CharField(max_length=100)
    Congregations = models.IntegerField(default=0)
    Adherents = models.IntegerField(default=0)
    Adherents_percent_of_Total_Adherents = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))
    Adherents_percent_of_Population = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "State"
        db_table = "by_state"


# filter out manually
# churchStates = State.objects.count()




##  BY COUNTY MODEL
class County(models.Model):
    # id = django_mongodb_backend.fields.ObjectIdAutoField(primary_key=True, editable=False) # Other fields in your model
    id = django_mongodb_backend.fields.ObjectIdAutoField
    StateCode = models.CharField(max_length=3)
    FIPS = models.IntegerField()
    GroupCode = models.CharField(max_length=5) ##mixed type issue
    Congregations = models.IntegerField(default=0)
    Adherents = models.IntegerField(default=0)
    Adherents_percent_of_Total_Adherents = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))
    Adherents_percent_of_Population = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))

    class Meta:
        verbose_name = "County"
        verbose_name_plural = "County"
        db_table = "by_county"

# filter out manually in calling code?
# churchCounties = County.objects.count()