import django.db.models as models


## TODO: refactor mixed field types or find model procs/code to fix on the fly?


## meta: Copyright © 2022 by the Association of Statisticians of American Religious Bodies (ASARB)


##
class Summary(models.Model):
    objectID = models.UUIDField(primary_key=True, editable=False)
    Population_2020 = models.IntegerField()
    Congregations = models.IntegerField()
    Adherents = models.IntegerField()
    Congregations_per_1000_Population = models.CharField(max_length=10)
    Adherents_percent_of_Population = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Summary"
        verbose_name_plural = "Summary"
        db_table = "summary"




## NATIONAL MODEL
class National(models.Model):
    objectID = models.UUIDField(primary_key=True, editable=False)

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

churchGroups = National.objects.count



## BY METRO MODEL
class Metro(models.Model):
    objectID = models.UUIDField(primary_key=True, editable=False)

    CBSACode = models.IntegerField()
    MetroName = models.CharField(max_length=100)
    GroupCode = models.CharField(max_length=5) ##mixed type issue
    GroupName = models.CharField(max_length=100)
    Congregations = models.IntegerField(default=0)
    Adherents = models.IntegerField(default=0)
    Adherents_percent_of_Total_Adherents = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    Adherents_percent_of_Population = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.MetroName} > {self.GroupName}, ({self.Congregations} congregations)"

    class Meta:
        verbose_name = "Metro"
        verbose_name_plural = "Metro"
        db_table = "by_metro"

churchMetros = Metro.objects.count('MetroName', distinct=True)



## BY STATE MODEL
class State(models.Model):
    objectID = models.UUIDField(primary_key=True, editable=False)

    StateCode = models.CharField(max_length=3)
    StateName = models.CharField(max_length=100)
    GroupCode = models.CharField(max_length=5) ##mixed type issue
    GroupName = models.CharField(max_length=100)
    Congregations = models.IntegerField(default=0)
    Adherents = models.IntegerField(default=0)
    Adherents_percent_of_Total_Adherents = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    Adherents_percent_of_Population = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.StateName} > {self.GroupName}, ({self.Congregations} congregations)"

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "State"
        db_table = "by_state"

churchStates = State.objects.count('StateName', distinct=True)




##  BY COUNTY MODEL
class County(models.Model):
    objectID = models.UUIDField(primary_key=True, editable=False)

    FIPS = models.IntegerField()
    StateName = models.CharField(max_length=100)
    CountyName = models.CharField(max_length=100)
    GroupCode = models.CharField(max_length=5) ##mixed type issue
    GroupName = models.CharField(max_length=100)
    Congregations = models.IntegerField(default=0)
    Adherents = models.IntegerField(default=0)
    Adherents_percent_of_Total_Adherents = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    Adherents_percent_of_Population = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.CountyName}, {self.StateName} > {self.GroupName}, ({self.Congregations} congregations)"

    class Meta:
        verbose_name = "County"
        verbose_name_plural = "County"
        db_table = "by_county"

churchCounties = County.objects.count('CountyName', distinct=True)