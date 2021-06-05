from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
# Create your models here.

class Skills(models.Model):
    name = models.CharField(max_length=100, null=False, default='')
    

class Experience(models.Model):

    company_name = models.CharField(max_length=200, null=False, default='')
    starting_date = models.CharField(max_length=200, null=False, default='')
    ending_date = models.CharField(max_length=200, null=True, blank=True, default='Present')
    job_title = models.CharField(max_length=200, null=False, default='')
    job_description = models.TextField(max_length=200, null=True,blank=True, default='')
    created_by = models.ForeignKey(User, related_name='experiences', null=True, on_delete=models.CASCADE)


class Education(models.Model):

    school = models.CharField(max_length=200, null=False, default='')
    starting_date = models.CharField(max_length=200, null=False, default='')
    ending_date = models.CharField(max_length=200, null=True, blank=True, default='Present')
    degree = models.CharField(max_length=200, null=False, default='')
    description = models.TextField(max_length=200, null=True,blank=True, default='')
    created_by = models.ForeignKey(User, related_name='educations', null=True, on_delete=models.CASCADE)

class UserProject(models.Model):
    project_title = models.CharField(max_length=300, null=False, default='')
    project_url = models.CharField(max_length=300, null=False, default='')
    created_by = models.ForeignKey(User, related_name='projects', null=True, on_delete=models.CASCADE)

class UserAward(models.Model):
    award_title = models.CharField(max_length=300, null=False, default='')
    award_date = models.CharField(max_length=300, null=False, default='')
    created_by = models.ForeignKey(User, related_name='awards', null=True, on_delete=models.CASCADE)




class Job(models.Model):
    jobTitle = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=500, blank=True, null=True)
    budget = models.CharField(max_length=300, default='')
    timeCreated = models.DateField(auto_now_add=True, null=True)
    duration = models.CharField(max_length=200, default='')
    experience = models.CharField(max_length=200, default='')
    proposal_count = models.IntegerField(max_length=1000, default=0)
    job_status = models.CharField(max_length=200, default='Open')
    awarded_to = models.ForeignKey(User, related_name='awarded', on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE)
    pending_amount = models.IntegerField(default=0, null=True)


class Review(models.Model):
    review_rating = models.FloatField(null=False, default=0.0)
    feedback = models.CharField(max_length=500, default='')
    given_to = models.ForeignKey(User, related_name='givento', null=True, on_delete=models.CASCADE)
    on_job = models.ForeignKey(Job, related_name='completed_job', null=True, on_delete=models.CASCADE)
    given_by = models.ForeignKey(User, related_name='givenby', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class Proposal(models.Model):
    amount = models.IntegerField( blank=False, null=True)
    bid = models.CharField(max_length=1000, blank=False)
    duration = models.CharField(max_length=200, default='')
    on_job = models.ForeignKey(Job, related_name='jobproposal', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='proposalsender', on_delete=models.CASCADE)
    timeCreated = models.DateField(null=True, auto_now_add=True) 


class Message(models.Model):
    application = models.ForeignKey(Proposal, related_name='proposalmessage', on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(User, related_name='messageuser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True,auto_now_add=True)

    class Meta:
        ordering = ['created_at']

class Report(models.Model):
    reason = CharField(max_length=200, default='', null=True)
    description = CharField(max_length=1000, default='')

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=False, null=False, default='')
    last_name = models.CharField(max_length=100, blank=False, null=False, default='')
    email = models.CharField(max_length=200, default='NA', null=False)
    hourly_rate = models.CharField(max_length=200,default='Enter Service Hourly Rate ($)')
    tag_line = models.TextField(default='Add Your Tagline Here')
    country = models.CharField(max_length=200, null=False, default='')
    feedback = models.IntegerField(null=False, default=0)
    skills = models.ManyToManyField(Skills, null=True, blank=True, related_name='skill')
    created_at = models.DateTimeField(null=True,auto_now_add=True)
    description = models.TextField(null=True, blank=True, default='Description')
    is_employer = models.BooleanField(default=False)
    balance = models.IntegerField(default=0)
    completed_jobs = models.IntegerField(default=0)
    ongoing_jobs = models.IntegerField(default=0)
    overall_rating = models.FloatField(default=0.0)



    

