from django.db import models
class login(models.Model):
	name=models.CharField(max_length=50)
	userid=models.CharField(max_length=20)
	email=models.CharField(max_length=50)
	ht=models.BooleanField(default="True");
	cnn=models.BooleanField(default="True");
	toi=models.BooleanField(default="True");
	nol=models.IntegerField(default=5)
	
def __st__(self):
	return {"userid":self.userid,"name":self.name,"email":self.email,}
#class login(models.Model):
#	name = models.CharField(max_length=30)
#	email = models.CharField(max_length=30)
#	password=models.CharField(max_length=100,blank=true)


# Create your models here.

