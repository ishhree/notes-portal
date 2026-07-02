from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import FileResponse
from django.contrib import messages

from .models import Note


# ---------------- HOME ----------------
@login_required(login_url='/login/')
def home(request):
    query = request.GET.get('q')

    if query:
        notes = Note.objects.filter(user=request.user, title__icontains=query) | \
                Note.objects.filter(user=request.user, subject__icontains=query)
    else:
        notes = Note.objects.filter(user=request.user)

    total_notes = notes.count()

    return render(request, 'home.html', {
        'notes': notes,
        'total_notes': total_notes
    })

    return render(request, 'home.html', {'notes': notes})


# ---------------- UPLOAD ----------------
@login_required(login_url='/login/')
def upload_note(request):
    if request.method == "POST":
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        pdf = request.FILES.get('pdf')
        image = request.FILES.get('image')

        Note.objects.create(
            user=request.user,
            title=title,
            subject=subject,
            description=description,
            pdf=pdf,
            image=image
        )
        return redirect('home')

    return render(request, 'upload.html')


# ---------------- EDIT ----------------
@login_required(login_url='/login/')
def edit_note(request, id):
    note = get_object_or_404(Note, id=id, user=request.user)

    if request.method == "POST":
        note.title = request.POST['title']
        note.subject = request.POST['subject']
        note.description = request.POST['description']

        if request.FILES.get('pdf'):
            note.pdf = request.FILES['pdf']

        note.save()
        return redirect('home')

    return render(request, 'edit.html', {'note': note})


# ---------------- DELETE ----------------
@login_required(login_url='/login/')
def delete_note(request, id):
    note = get_object_or_404(Note, id=id, user=request.user)
    note.delete()
    return redirect('home')


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("LOGIN SUCCESS")
            print(request.user.is_authenticated)
            return redirect('home')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------- REGISTER ----------------


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')

#-----------admin dash-------------------
def adminboard(request):
    total_notes = Note.objects.count()
    total_users = User.objects.count()

    return render(request, 'adminboard.html', {
        'total_notes': total_notes,
        'total_users': total_users,
    })


#--favourites--
def favorites(request):
    notes = Note.objects.filter(is_favorite=True)
    return render(request, 'favorites.html', {'notes': notes})
def toggle_fav(request, id):
    note = Note.objects.get(id=id)
    note.is_favorite = not note.is_favorite
    note.save()
    return redirect('favorites')

# ---------------- vieww(open pdf) ----------------
def open_pdf(request, id):
    note = get_object_or_404(Note, id=id)

    response = FileResponse(note.pdf.open(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline'; filename="file.pdf"
    return response

# ---------------- THEME ----------------
