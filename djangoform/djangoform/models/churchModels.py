from decimal import Decimal
import django.db.models as models
from djangoform.api import model_manager as mgr
import django_mongodb_backend.fields


## meta: Copyright © 2022 by the Association of Statisticians of American Religious Bodies (ASARB)


class Summary(models.Model):
    """
    Summary data model for USRC 2020 data
    """
    id = django_mongodb_backend.fields.ObjectIdAutoField(primary_key=True, editable=False)
    Population_2020 = models.IntegerField()
    Congregations = models.IntegerField()
    Adherents = models.IntegerField()
    Congregations_per_1000_Population = models.CharField(max_length=10)
    Adherents_percent_of_Population = models.DecimalField(max_digits=5, decimal_places=2)
    modelMgr = mgr.USRC2020_ModelManager()
    allData = modelMgr.all()

    class Meta:
        verbose_name = "Summary"
        verbose_name_plural = "Summary"
        db_table = "summary"




## NATIONAL MODEL
class National(models.Model):
    id = django_mongodb_backend.fields.ObjectIdAutoField(primary_key=True, editable=False)

    GroupCode = models.CharField(max_length=5) ##mixed type issue
    GroupName = models.CharField(max_length=100)
    Congregations = models.IntegerField()
    Adherents = models.IntegerField()
    Adherents_percent_of_Total_Adherents = models.DecimalField(max_digits=5, decimal_places=2)
    Adherents_percent_of_Population = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.GroupName}, ({self.Congregations} congregations)"

    class Meta:
        verbose_name = "National"
        verbose_name_plural = "National"
        db_table = "national"

# churchGroups = National.objects.count()



## BY METRO MODEL
class Metro(models.Model):
    id = django_mongodb_backend.fields.ObjectIdAutoField(primary_key=True, editable=False)

    CBSACode = models.IntegerField()
    MetroName = models.CharField(max_length=100)
    GroupCode = models.CharField(max_length=5) ##mixed type issue
    GroupName = models.CharField(max_length=100)
    Congregations = models.IntegerField(default=0)
    Adherents = models.IntegerField(default=0)
    Adherents_percent_of_Total_Adherents = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))
    Adherents_percent_of_Population = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))

    def __str__(self):
        return f"{self.MetroName} > {self.GroupName}, ({self.Congregations} congregations)"

    class Meta:
        verbose_name = "Metro"
        verbose_name_plural = "Metro"
        db_table = "by_metro"

# gonna need to filter this out manually
# churchMetros = Metro.objects.count()



## BY STATE MODEL
class State(models.Model):
    id = django_mongodb_backend.fields.ObjectIdAutoField(primary_key=True, editable=False)

    StateCode = models.CharField(max_length=3)
    StateName = models.CharField(max_length=100)
    GroupCode = models.CharField(max_length=5) ##mixed type issue
    GroupName = models.CharField(max_length=100)
    Congregations = models.IntegerField(default=0)
    Adherents = models.IntegerField(default=0)
    Adherents_percent_of_Total_Adherents = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))
    Adherents_percent_of_Population = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))

    def __str__(self):
        return f"{self.StateName} > {self.GroupName}, ({self.Congregations} congregations)"

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "State"
        db_table = "by_state"


# filter out manually
# churchStates = State.objects.count()




##  BY COUNTY MODEL
class County(models.Model):
    # id = django_mongodb_backend.fields.ObjectIdAutoField(primary_key=True, editable=False) # Other fields in your model
    id = django_mongodb_backend.fields.ObjectIdAutoField(primary_key=True, editable=False)

    FIPS = models.IntegerField()
    StateName = models.CharField(max_length=100)
    CountyName = models.CharField(max_length=100)
    GroupCode = models.CharField(max_length=5) ##mixed type issue
    GroupName = models.CharField(max_length=100)
    Congregations = models.IntegerField(default=0)
    Adherents = models.IntegerField(default=0)
    Adherents_percent_of_Total_Adherents = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))
    Adherents_percent_of_Population = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))

    def __str__(self):
        return f"{self.CountyName}, {self.StateName} > {self.GroupName}, ({self.Congregations} congregations)"

    class Meta:
        verbose_name = "County"
        verbose_name_plural = "County"
        db_table = "by_county"

# filter out manually in calling code?
# churchCounties = County.objects.count()