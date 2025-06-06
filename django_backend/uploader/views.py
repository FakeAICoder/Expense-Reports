from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def process_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # Placeholder for processing logic, e.g., parsing expense report
        # For now we just read the file name
        print(f"Received file: {uploaded_file.name}")
        return HttpResponse('File processed')
    return HttpResponse('No file received', status=400)
