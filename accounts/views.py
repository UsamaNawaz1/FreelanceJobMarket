
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views import View
import stripe, json
from .models import Education, Job, Skills, UserAward, Userprofile, Experience, Education, UserProject, UserAward, Job, Proposal, Message, Review, Report

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
    # Invalid signature
        return HttpResponse(status=400)


    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        
        winner_id =  session["metadata"]["winner_id"]
        job_id =  session["metadata"]["job_id"]
        job = Job.objects.get(pk=job_id)
        winner = Proposal.objects.get(pk=winner_id)
        job.awarded_to = winner.created_by
        job.job_status = 'Ongoing'
        job.created_by.userprofile.ongoing_jobs = job.created_by.userprofile.ongoing_jobs + 1
        job.created_by.userprofile.save()
        winner.created_by.userprofile.ongoing_jobs = winner.created_by.userprofile.ongoing_jobs + 1
        winner.created_by.userprofile.save()
        job.pending_amount = winner.amount
        job.save()
        message = Message.objects.create(application=winner,created_by=job.created_by, content=f'{job.created_by.userprofile.first_name} has awarded you the project with title {job.jobTitle}')
        message.save()
        
        
        

    return HttpResponse(status=200)


def checkout(request, job_id, winner_id):
    job = Job.objects.get(pk=job_id)
    winner = Proposal.objects.get(pk=winner_id)

    context = {
        'job' : job,
        'winner' : winner,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
    }
    

    return render(request, 'accounts/landing.html', context)

class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        #http://127.0.0.1:8000
        #https://vegassportsadvantage-1.herokuapp.com/
        #https://www.vegassportsadvantage.com
        YOUR_DOMAIN = 'http://127.0.0.1:8000'
        job_id = kwargs['job_id']
        winner_id = kwargs['winner_id']
        job = Job.objects.get(pk=job_id)
        winner = Proposal.objects.get(pk=winner_id)
        checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': winner.amount * 100,
                            'product_data': {
                                'name': job.jobTitle,
                                
                            },
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    'job_id':job_id,
                    'winner_id':winner_id,
                },
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
        return JsonResponse({'id': checkout_session.id})



def paypal_complete(request):
    
    body = json.loads(request.body)
    print('BODY: ',body)
    job_id = body["job_id"]
    winner_id = body["winner_id"]
    
    job = Job.objects.get(pk=job_id)
    winner = Proposal.objects.get(pk=winner_id)
    job.awarded_to = winner.created_by
    job.job_status = 'Ongoing'
    job.created_by.userprofile.ongoing_jobs = job.created_by.userprofile.ongoing_jobs + 1
    job.created_by.userprofile.save()
    winner.created_by.userprofile.ongoing_jobs = winner.created_by.userprofile.ongoing_jobs + 1
    winner.created_by.userprofile.save()
    job.pending_amount = winner.amount
    job.save()
    message = Message.objects.create(application=winner,created_by=job.created_by, content=f'{job.created_by.userprofile.first_name} has awarded you the project with title {job.jobTitle}')
    message.save()

    return redirect('success')


def success(request):
    return render(request, 'accounts/success.html')


def cancel(request):
    return render(request, 'accounts/cancel.html')


def message(request, job_id, proposal_id):
    job = Job.objects.get(pk=job_id)
    proposal = Proposal.objects.get(pk=proposal_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        message = Message.objects.create(content=content, application=proposal, created_by=request.user)
        message.save()
    context = {
        'job':job,
        'prop' : proposal,
    }
    return render(request, 'accounts/message.html', context)

def freelancer_proposal(request):
    return render(request, 'accounts/freelancer_proposal.html')


def view_proposal(request, job_id, proposal_id):
    job = Job.objects.get(pk=job_id)
    proposal = Proposal.objects.get(pk=proposal_id)
    context = {
        'job':job,
        'proposal' : proposal,
    }
    return render(request, 'accounts/view_proposal.html', context)



def job_completed(request, job_id):
    job = Job.objects.get(pk=job_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')


        if request.user.userprofile.is_employer:

            review = Review.objects.create(review_rating=rating, feedback=feedback, given_by=job.created_by,on_job=job, given_to=job.awarded_to)
            review.save()


            job.job_status = 'Completed'
            total_reviews = Review.objects.filter(given_to=job.awarded_to)
            temp = 0.0
            size = len(total_reviews)
            for x in total_reviews:
                temp += x.review_rating
            job.awarded_to.userprofile.overall_rating = round(temp/size,1)
            job.awarded_to.userprofile.feedback = job.awarded_to.userprofile.feedback + 1
            
            job.created_by.userprofile.completed_jobs = job.created_by.userprofile.completed_jobs + 1
            job.created_by.userprofile.save()
            
            job.awarded_to.userprofile.completed_jobs = job.awarded_to.userprofile.completed_jobs + 1
            job.awarded_to.userprofile.balance = job.pending_amount - (job.pending_amount * 0.1)
            job.awarded_to.userprofile.save()
            job.save()
        else:   
            review = Review.objects.create(review_rating=rating, feedback=feedback, given_by=job.awarded_to,on_job=job, given_to=job.created_by)
            review.save()
            job.job_status = 'Completed'
            total_reviews = Review.objects.filter(given_to=job.created_by)
            temp = 0.0
            size = len(total_reviews)
            for x in total_reviews:
                temp += x.review_rating
            job.created_by.userprofile.overall_rating = round(temp/size,1)
            job.created_by.userprofile.feedback = job.created_by.userprofile.feedback + 1
            job.created_by.userprofile.save()

        return redirect('manage_jobs')

    return render(request, 'accounts/job_completed.html')

def job_proposal(request, job_id):
    job = Job.objects.get(pk=job_id)
    
    return render(request, 'accounts/job_proposal.html', {'job':job})

def add_proposal(request, job_id):
    job = Job.objects.get(pk=job_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        bid = request.POST.get('bid')
        
        duration = request.POST.get('duration')
        
        proposal = Proposal.objects.create(amount=amount, bid=bid, duration=duration, created_by=request.user, on_job=job)
        proposal.save()
        job.proposal_count = job.proposal_count + 1
        job.save()
        return redirect('freelancer_proposal')
    return render(request, 'accounts/add_proposal.html', {'job':job})

def manage_jobs(request):
    return render(request, 'accounts/manage_jobs.html')

def about(request):
    return render(request, 'accounts/about.html')
    
def how_work(request):
    return render(request, 'accounts/how_work.html')

def jobs(request):
    jobs = Job.objects.all()
    context={
        'jobs':jobs,
    }
    return render(request, 'accounts/jobs.html', context)


def view_freelancers(request):
    freelancers = Userprofile.objects.filter(is_employer=False)
    context={
        'freelancers':freelancers,
    }
    return render(request, 'accounts/view_freelancers.html', context)

def freelancer(request, pk):
    
    userprofile = Userprofile.objects.get(pk=pk)
    reviews = Review.objects.filter(given_to=userprofile.user)
    educations = Education.objects.filter(created_by=userprofile.user)
    projects = UserProject.objects.filter(created_by=userprofile.user)
    awards = UserAward.objects.filter(created_by=userprofile.user)
    experiences = Experience.objects.filter(created_by=userprofile.user)
    context={
        'freelancer':userprofile,
        'educations':educations,
        'projects':projects,
        'experiences':experiences,
        'awards':awards,
        'reviews':reviews
    }
    return render(request, 'accounts/freelancer.html', context)


def home(request):
    return render(request, 'accounts/index-2.html')

def job_single(request, pk):
    job = Job.objects.get(pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        description = request.POST.get('description')
        report = Report.objects.create(reason=reason, description=description)
        report.save()
    check = False
    
    if request.user.userprofile.is_employer == False:
        proposals = Proposal.objects.filter(created_by=request.user)
        for proposal in proposals:
            if proposal.on_job.id == job.id:
                check = True
    return render(request, 'accounts/job_single.html', {'job':job, 'check':check})

def addJobs(request):
    if request.method == 'POST':
        jobTitle = request.POST.get('jobTitle')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        experience = request.POST.get('experience')
        budget = request.POST.get('budget')
        
        job = Job.objects.create(jobTitle=jobTitle, description=description, duration=duration, experience=experience, created_by=request.user, budget=budget)
        job.save()
        return redirect('jobs')
    return render(request, 'accounts/addJobs.html')

def profile(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'accounts/profile.html', {'user': user})


def user_account(request):
    skills = request.user.userprofile.skills.all
    exp = request.user.experiences.all
    edu = request.user.educations.all
    pro = request.user.projects.all
    awr = request.user.awards.all
    job = 1
    proposal = 1
    check = False
    if request.user.userprofile.is_employer == False:
        proposal = Proposal.objects.filter(created_by=request.user)
        if len(proposal) > 0:
            proposal = proposal[0]
            job_id = proposal.on_job.id
            job = Job.objects.get(pk=job_id)
            check = True
    if request.method == 'POST':
        request.user.userprofile.first_name = request.POST.get('first_name')
        request.user.userprofile.last_name = request.POST.get('last_name')
        request.user.userprofile.hourly_rate = request.POST.get('hourly_rate')
        
        request.user.userprofile.tag_line = request.POST.get('tag_line')
        request.user.userprofile.description = request.POST.get('description')
        request.user.userprofile.save()
    context = {
        'skills':skills,
        'works':exp,
        'learning': edu,
        'projects':pro,
        'awards' : awr,
        'job': job,
        'proposal':proposal,
        'check':check,
    }
    return render(request, 'accounts/user_account.html', context)


def addSkills(request, pk):
    user= User.objects.get(pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('Skills')
        skill = Skills.objects.get(name=name)
        user.userprofile.skills.add(skill)
        user.userprofile.save()

    
    return redirect('user_account')

def addExperience(request, pk):
    user= User.objects.get(pk=pk)
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        starting_date = request.POST.get('starting_date')
        ending_date = request.POST.get('ending_date')
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        
        exp = Experience.objects.create(company_name=company_name, starting_date=starting_date, ending_date=ending_date, job_title=job_title, job_description=job_description, created_by=user)
        exp.save()
        return redirect('user_account')
    
    return redirect('user_account')


def addEducation(request, pk):
    user= User.objects.get(pk=pk)
    if request.method == 'POST':
        company_name = request.POST.get('school')
        starting_date = request.POST.get('starting_date')
        ending_date = request.POST.get('ending_date')
        job_title = request.POST.get('degree')
        job_description = request.POST.get('description')
        
        edu = Education.objects.create(school=company_name, starting_date=starting_date, ending_date=ending_date, degree=job_title, description=job_description, created_by=user)
        edu.save()
        return redirect('user_account')
    
    return redirect('user_account')

def addProject(request, pk):
    user= User.objects.get(pk=pk)
    if request.method == 'POST':
        project_title = request.POST.get('project_title')
        project_url = request.POST.get('project_url')
        
        
        pro = UserProject.objects.create(project_title=project_title, project_url=project_url, created_by=user)
        pro.save()
        return redirect('user_account')
    
    return redirect('user_account')


def addAward(request, pk):
    user= User.objects.get(pk=pk)
    if request.method == 'POST':
        award_title = request.POST.get('award_title')
        award_date = request.POST.get('award_date')
        
        
        awr = UserAward.objects.create(award_title=award_title, award_date=award_date, created_by=user)
        awr.save()
        return redirect('user_account')
    
    return redirect('user_account')


def coming_soon(request):
    return render(request, 'accounts/coming_soon.html')


def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.email = request.POST.get('email')
            user.save()
            
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            account_type = request.POST.get('account_type', 'jobseeker')
            country = request.POST.get('country')

            if account_type == 'employee':
                userprofile = Userprofile.objects.create(user = user, first_name=first_name, last_name=last_name, country=country, is_employer = True)
                userprofile.save()
            else:
                userprofile = Userprofile.objects.create(user = user, first_name=first_name, last_name=last_name, country=country)
                userprofile.save()

            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form':form})


def loginPage(request):
    data = dict()
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            
            messages.error(request, "username or password is incorrect")
 
    return render(request, 'accounts/login.html', data)

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')