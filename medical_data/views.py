import os
import json
import uuid
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from .forms import MedicalRecordForm, JSONUploadForm
from .models import MedicalRecord, JSONFile

def home(request):
    return render(request, 'medical_data/home.html')

def create_medical_record(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record_id = uuid.uuid4()
            json_data = {
                'id': str(record_id),
                'patient_name': form.cleaned_data['patient_name'],
                'age': form.cleaned_data['age'],
                'gender': form.cleaned_data['gender'],
                'height': form.cleaned_data['height'],
                'weight': form.cleaned_data['weight'],
                'blood_pressure': form.cleaned_data['blood_pressure'],
                'heart_rate': form.cleaned_data['heart_rate'],
                'temperature': form.cleaned_data['temperature'],
                'symptoms': form.cleaned_data['symptoms'],
                'diagnosis': form.cleaned_data['diagnosis'],
                'created_at': timezone.now().isoformat()
            }
            
            json_dir = os.path.join(settings.MEDIA_ROOT, 'medical_json')
            os.makedirs(json_dir, exist_ok=True)
            
            filename = f"medical_record_{record_id}.json"
            filepath = os.path.join(json_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            messages.success(request, f'Медицинская запись сохранена в файл: {filename}')
            return redirect('view_json_files')
    else:
        form = MedicalRecordForm()
    
    return render(request, 'medical_data/create_record.html', {'form': form})

def upload_json_file(request):
    if request.method == 'POST':
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = form.save(commit=False)
            
            try:
                file_content = json_file.file.read().decode('utf-8')
                data = json.loads(file_content)
                
                required_fields = ['patient_name', 'age', 'gender', 'height', 'weight']
                for field in required_fields:
                    if field not in data:
                        raise ValueError(f"Отсутствует обязательное поле: {field}")
                
                json_file.is_valid = True
                json_file.save()
                
                messages.success(request, 'Файл успешно загружен и проверен!')
                
            except (json.JSONDecodeError, ValueError, UnicodeDecodeError) as e:
                if json_file.file:
                    if os.path.isfile(json_file.file.path):
                        os.remove(json_file.file.path)
                messages.error(request, f'Ошибка в файле: {str(e)}')
                return redirect('upload_json')
            
            return redirect('view_json_files')
    else:
        form = JSONUploadForm()
    
    return render(request, 'medical_data/upload_json.html', {'form': form})
def view_json_files(request):
    json_dir = os.path.join(settings.MEDIA_ROOT, 'medical_json')
    
    if not os.path.exists(json_dir):
        messages.info(request, 'Папка с JSON файлами не существует.')
        return render(request, 'medical_data/view_files.html', {'files': []})
    
    json_files = []
    try:
        for filename in os.listdir(json_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(json_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        json_files.append({
                            'filename': filename,
                            'data': data,
                            'filepath': filepath,
                            'size': os.path.getsize(filepath)
                        })
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
    except FileNotFoundError:
        messages.info(request, 'Папка с JSON файлами не найдена.')
    
    if not json_files:
        messages.info(request, 'Нет доступных JSON файлов.')
    
    return render(request, 'medical_data/view_files.html', {'files': json_files})

def view_medical_records(request):
    json_dir = os.path.join(settings.MEDIA_ROOT, 'medical_json')
    
    if not os.path.exists(json_dir):
        messages.info(request, 'Папка с JSON файлами не существует.')
        return render(request, 'medical_data/view_records.html', {'records': []})
    
    records = []
    try:
        for filename in os.listdir(json_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(json_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        record_data = {
                            'filename': filename,
                            'filepath': filepath,
                            'size': os.path.getsize(filepath),
                            'data': data  
                        }
                        records.append(record_data)
                        
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
        
        records.sort(key=lambda x: x['data'].get('created_at', ''), reverse=True)
        
    except FileNotFoundError:
        messages.info(request, 'Папка с JSON файлами не найдена.')
    
    if not records:
        messages.info(request, 'Нет доступных медицинских записей.')
    
    return render(request, 'medical_data/view_records.html', {'records': records})
