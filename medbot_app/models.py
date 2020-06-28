from django.db import models

class Inventory(models.Model):
	"""docstring for Inventory"""
	MUSTPRESCRIBED = 'MP'
	MUSTNOTPRESCRIBE = 'MNP'
	MEDICINESTATUS = [
		(MUSTPRESCRIBED, 'Must be Prescribed'),
		(MUSTNOTPRESCRIBE, 'Must not be Prescribed'),
	]
			
	med_name = models.CharField(max_length = 200)
	med_status = models.BooleanField(default = False)
	med_id = models.BigAutoField(primary_key = True, serialize=False)
	med_price = models.FloatField(max_length = 10)
	med_quantity = models.PositiveIntegerField()
	med_status = models.CharField(max_length = 10, choices = MEDICINESTATUS, default=MUSTPRESCRIBED)
	med_catagory = models.CharField(max_length = 100)

	def is_upperclass(self):
        return self.year_in_school in {self.MUSTPRESCRIBED, self.MUSTNOTPRESCRIBE}

		
