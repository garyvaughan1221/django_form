import django.db.models as models

class ByCounty(models.Model):
    id = models.BigAutoField(primary_key=True)
    statecode = models.ForeignKey('StateNames', models.DO_NOTHING, db_column='StateCode')  # Field name made lowercase.
    fips = models.IntegerField(db_column='FIPS')  # Field name made lowercase.
    groupcode = models.ForeignKey('ChurchOrgs', models.DO_NOTHING, db_column='GroupCode')  # Field name made lowercase.
    congregations = models.IntegerField(db_column='Congregations', blank=True, null=True)  # Field name made lowercase.
    adherents = models.IntegerField(db_column='Adherents', blank=True, null=True)  # Field name made lowercase.
    adherents_percent_of_total_adherents = models.FloatField(db_column='Adherents_percent_of_Total_Adherents', blank=True, null=True)  # Field name made lowercase.
    adherents_percent_of_population = models.FloatField(db_column='Adherents_percent_of_Population', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'by_county'


class ByState(models.Model):
    id = models.BigAutoField(primary_key=True)
    statecode = models.ForeignKey('StateNames', models.DO_NOTHING, db_column='StateCode')  # Field name made lowercase.
    groupcode = models.CharField(db_column='GroupCode', max_length=3)  # Field name made lowercase.
    congregations = models.IntegerField(db_column='Congregations', blank=True, null=True)  # Field name made lowercase.
    adherents = models.IntegerField(db_column='Adherents', blank=True, null=True)  # Field name made lowercase.
    adherents_percent_of_total_adherents = models.FloatField(db_column='Adherents_percent_of_Total_Adherents', blank=True, null=True)  # Field name made lowercase.
    adherents_percent_of_population = models.FloatField(db_column='Adherents_percent_of_Population', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_state'


class ChurchOrgs(models.Model):
    groupname = models.CharField(db_column='GroupName', unique=True, max_length=111)  # Field name made lowercase.
    groupcode = models.CharField(db_column='GroupCode', primary_key=True, max_length=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'church_orgs'


class CountyNames(models.Model):
    statecode = models.ForeignKey('StateNames', models.DO_NOTHING, db_column='StateCode')  # Field name made lowercase.
    countyname = models.CharField(db_column='CountyName', max_length=33)  # Field name made lowercase.
    fips = models.IntegerField(db_column='FIPS', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'county_names'


class National(models.Model):
    groupcode = models.CharField(db_column='GroupCode', max_length=3)  # Field name made lowercase.
    congregations = models.IntegerField(db_column='Congregations', blank=True, null=True)  # Field name made lowercase.
    adherents = models.IntegerField(db_column='Adherents', blank=True, null=True)  # Field name made lowercase.
    adherents_percent_of_total_adherents = models.FloatField(db_column='Adherents_percent_of_Total_Adherents', blank=True, null=True)  # Field name made lowercase.
    adherents_percent_of_population = models.FloatField(db_column='Adherents_percent_of_Population', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'national'


class StateNames(models.Model):
    statecode = models.CharField(db_column='StateCode', primary_key=True, max_length=2)  # Field name made lowercase.
    statename = models.CharField(db_column='StateName', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'state_names'