import requests
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Story, Contribution, Comment, Like
from .forms import CustomUserCreationForm  # Yeni formu içe aktar
import google.generativeai as genai
from io import BytesIO
from django.core.files.base import ContentFile


def story_list(request):
    ongoing_stories = Story.objects.filter(is_complete=False)
    completed_stories = Story.objects.filter(is_complete=True)
    return render(request, "stories/story_list.html", {
        "ongoing_stories": ongoing_stories,
        "completed_stories": completed_stories
    })

@login_required
def new_story(request):
    if request.method == "POST":
        title = request.POST.get("title", "Unnamed Story")
        genre = request.POST.get("genre", "")
        max_contributors = int(request.POST.get("max_contributors", 5))
        Story.objects.create(title=title, genre=genre, max_contributors=max_contributors)
        return redirect("story_list")
    return render(request, "stories/new_story.html")

@login_required
def story_detail(request, story_id):
    story = Story.objects.get(id=story_id)
    contributions = Contribution.objects.filter(story=story)
    inputs = [c.user_input for c in contributions]

    if request.method == "POST":
        new_input = request.POST.get("user_input")
        user_contributions = Contribution.objects.filter(story=story, user=request.user).count()
        if contributions.count() < story.max_contributors and new_input and len(new_input) <= 200 and user_contributions < 2:
            Contribution.objects.create(story=story, user=request.user, user_input=new_input)
            return redirect("story_detail", story_id=story_id)

    story_text = story.text
    story_image = getattr(story, 'image', None)

    if not story_text and contributions.count() >= story.max_contributors and not story.is_complete:
        # Gemini API ile hikâye oluştur
        api_key = ""
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        prompt = (
            f"Bana '{story.title}' adında bir hikâye oluştur. "
            f"Türü '{story.genre}' olsun. "
            f"Hikâyende şu konuları, bilgileri de kullan: {', '.join(inputs)}."
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 2000}
        }
        headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            story_text = data["candidates"][0]["content"]["parts"][0]["text"]

            # Stable Diffusion ile görsel üret
            image_api_key = ""  # Hugging Face token’ını buraya koy
            image_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
            
            image_prompt = f"A {story.genre} scene inspired by '{story.title}': {story_text[:200]}"
            image_payload = {
                "inputs": image_prompt,
            }
            image_headers = {
                "Authorization": f"Bearer {image_api_key}",
                "Content-Type": "application/json"
            }
            image_response = requests.post(image_url, json=image_payload, headers=image_headers)
            image_response.raise_for_status()

            # Görseli dosyaya kaydet
            story_image_data = image_response.content  # Binary veri
            story_image = ContentFile(story_image_data, name=f"{story.title}.jpg")

            # Hikâyeyi ve görseli kaydet
            story.text = story_text
            story.image = story_image
            story.is_complete = True
            story.save()

        except requests.exceptions.RequestException as e:
            story_text = f"API hatası: {str(e)}"
        except Exception as e:
            story_text = f"Hata: {str(e)}"

    # Hikâyede katkıları vurgula
    if story_text:
        for input_text in inputs:
            story_text = story_text.replace(input_text, f"<strong>{input_text}</strong>")

    return render(request, "stories/story_detail.html", {
        "story": story,
        "contributions": contributions,
        "story_text": story_text,
        "story_image": story.image if story_image else None
    })



@login_required
def add_comment(request, story_id):
    if request.method == "POST":
        story = Story.objects.get(id=story_id)
        text = request.POST.get("comment_text")
        if text:
            Comment.objects.create(story=story, user=request.user, text=text)
    return redirect("story_detail", story_id=story_id)

@login_required
def add_like(request, story_id):
    story = Story.objects.get(id=story_id)
    if not Like.objects.filter(story=story, user=request.user).exists():
        Like.objects.create(story=story, user=request.user)
    return redirect("story_detail", story_id=story_id)

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("story_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "stories/register.html", {"form": form})
