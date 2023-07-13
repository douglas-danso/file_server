from django.shortcuts import render, redirect, get_object_or_404
from fileapp.forms import FileForm,SendFileForm
from fileapp.models import File
from django.views.generic import ListView
from django.core.mail import EmailMessage
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from authentication.models import CustomUser
from django.http import HttpResponseForbidden,HttpResponse
from django.shortcuts import render
from django.http import FileResponse
from .thumbnails import generate_thumbnail
from django.core.files.base import ContentFile




@login_required
def upload_file(request):
    user = CustomUser.objects.get(pk=request.user.pk)
    if user.is_superuser:
        if request.method == 'POST':
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.save()
                file.user_id = request.user.id
                file.save()
                if file.file.name.lower().endswith('.pdf'): 
                    file = form.save()
                    file.user = request.user
                    file_path = file.file.path  # Full file path
                    thumbnail = generate_thumbnail(file_path)
            
                    file.thumbnail.save(f'{file.title}_thumbnail.jpg', ContentFile(thumbnail))
                else:
                    form.save()
                return redirect('fileapp:upload_list')
        else:
            form = FileForm()
        return render(request, 'fileapp/upload_file.html', {'form': form})
    else:
        return HttpResponseForbidden('<h1> You are not authorised to view this page</h1>')

@login_required
def download_file(request, file_id):
    file = File.objects.get(pk=file_id)
    response = FileResponse(file.file, as_attachment=True)
    file.downloads += 1
    file.save()
    return response

    

@login_required
def send_file_email(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    if request.method == 'POST':
        form = SendFileForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = EmailMessage(
                subject,
                message,
                'douglasdanso66@gmail.com',
                [recipient_email],
                # ['bcc@example.com'],
                reply_to=['another@example.com']
            )
            email.attach_file(file.file.path)
            email.send()
            file.emails_sent += 1
            file.save()
            return redirect('fileapp:upload_list')
    else:
        form = SendFileForm()
    return render(request, 'fileapp/send_file.html', {'form': form, 'file': file})



@method_decorator(login_required, name='dispatch')
class FileListView(ListView):
    model = File
    template_name = 'fileapp/upload_list.html'
    context_object_name = 'files'
    ordering = ['title']
    paginate_by = 20
    
@method_decorator(login_required, name='dispatch')
class FileDetailView(DetailView):
    model = File
    template_name = 'fileapp/file_detail.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file'] = self.get_object()
        return context

@login_required
def logs(request):
    user = CustomUser.objects.get(pk=request.user.pk)
    if user.is_superuser:
        files = File.objects.all()
        return render(request, 'fileapp/logs.html',{'files':files})
    else:
        return HttpResponseForbidden('<h1> You are not authorised to view this page</h1>')
        
@login_required
def search_view(request):
    query = request.GET.get('q')
    if query:
        files = File.objects.filter(title__icontains=query)
    else:
        files = []
    return render(request, 'fileapp/search.html', {'files': files})


@login_required
def preview(request, file_id):
    file = get_object_or_404(File, id=file_id)

    if file.file.name.lower().endswith('.pdf'):
        return FileResponse(open(file.file.path, 'rb'), content_type='application/pdf')
    else:
        return render(request, 'fileapp/preview.html', {'file': file})
@login_required
def open_page(request, file_id):
    file = get_object_or_404(File, id=file_id)
    return render(request, 'fileapp/open_page.html',{'file': file})