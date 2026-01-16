from django.core.management.base import BaseCommand
from core.models import Question, Choice

class Command(BaseCommand):
    help = 'Seeds database with sample questions'

    def handle(self, *args, **options):
        Question.objects.all().delete()
        
        questions_data = [
            ("What activity do you enjoy most?", [
                ("Drawing and sketching layouts", "Design"),
                ("Solving logic puzzles", "Backend"),
                ("Building interactive UI components", "Frontend"),
                ("Using apps on my phone", "Mobile")
            ]),
            ("Which tool sounds more interesting?", [
                ("Figma / Adobe XD", "Design"),
                ("PostgreSQL / Docker", "Backend"),
                ("React / Vue.js", "Frontend"),
                ("Flutter / Swift", "Mobile")
            ]),
             ("When browsing a website, what do you notice first?", [
                ("The colors and typography", "Design"),
                ("How fast it loads data", "Backend"),
                ("The animations and layout", "Frontend"),
                ("How it looks on mobile", "Mobile")
            ]),
            ("You want to build a feature. Where do you start?", [
                ("Designing the mockup", "Design"),
                ("Designing the database schema", "Backend"),
                ("Coding the HTML/CSS structure", "Frontend"),
                ("Setting up the mobile view", "Mobile")
            ]),
        ]
        
        # Multiply to get 20 (just repeating for demo purposes, in real app need distinct q's)
        final_questions = questions_data * 5 
        
        for idx, (q_text, choices) in enumerate(final_questions):
            q = Question.objects.create(text=f"{idx+1}. {q_text}", category="Frontend") # Category here is just default, not important for logic
            for c_text, c_cat in choices:
                Choice.objects.create(question=q, text=c_text, weight_category=c_cat, weight_value=5)
                
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(final_questions)} questions.'))
