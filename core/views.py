from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.cache import cache
from .models import UserProfile, Question, Choice, Result
from .utils import generate_otp, generate_token
import json

def landing(request):
    return render(request, 'landing.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        
        # Create or Get User directly
        user, created = UserProfile.objects.get_or_create(
            phone_number=phone,
            defaults={'name': name}
        )
        
        # Log user in (using session)
        request.session['user_id'] = user.id
        
        return redirect('test_page')
    
    return render(request, 'register.html')

def test_page(request):
    if 'user_id' not in request.session:
        return redirect('register')
    return render(request, 'test.html')

def get_questions(request):
    questions = Question.objects.all()
    data = []
    for q in questions:
        choices = [{'id': c.id, 'text': c.text} for c in q.choices.all()]
        data.append({
            'id': q.id,
            'text': q.text,
            'image': q.image.url if q.image else None,
            'choices': choices
        })
    return JsonResponse({'questions': data})

def submit_test(request):
    if request.method == 'POST':
        if 'user_id' not in request.session:
             return JsonResponse({'error': 'Unauthorized'}, status=401)
             
        data = json.loads(request.body)
        answers = data.get('answers', [])
        
        scores = {'Frontend': 0, 'Backend': 0, 'Design': 0, 'Mobile': 0}
        
        for ans in answers:
            choice_id = ans.get('choice_id')
            try:
                choice = Choice.objects.get(id=choice_id)
                scores[choice.weight_category] += choice.weight_value
            except Choice.DoesNotExist:
                continue
                
        # Determine top category
        top_category = max(scores, key=scores.get)
        
        user = UserProfile.objects.get(id=request.session['user_id'])
        user.test_status = True
        user.save()
        
        result = Result.objects.create(
            user=user,
            scores=scores,
            top_category=top_category
        )
        
        return JsonResponse({'redirect_url': '/result/'})
    return JsonResponse({'error': 'Invalid method'}, status=400)

def result_page(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('landing')
        
    result = Result.objects.filter(user_id=user_id).last()
    if not result:
        return redirect('test_page')
        
    return render(request, 'result.html', {
        'result': result, 
        'scores': json.dumps(result.scores)
    })
