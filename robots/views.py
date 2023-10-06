from datetime import datetime, timedelta

import openpyxl
from io import BytesIO

from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Robot
import json

from collections import defaultdict


class CreatedRobotView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            model = data['model']
            version = data['version']
            created_str = data['created']

            # Проверяем форматирование
            if len(model) != 2:
                raise ValidationError('The model must contain two characters')
            if len(version) != 2:
                raise ValidationError('The version must contain two characters')
            try:
                created = datetime.strptime(created_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValidationError('Incorrect date format. Use format: YYYY-mm-dd HH:MM:SS')

            # Создаем серию на основе модели и версии
            serial = f"{model}-{version}"

            robot = Robot.objects.create(serial=serial, model=model, version=version, created=created)

            response_data = {'message': 'Robot created successfully'}
            return JsonResponse(response_data, status=201)
        except KeyError:
            response_data = {'message': 'Invalid data format'}
            x = JsonResponse(response_data, status=400)
            return x
        except ValidationError as e:
            response_data = {'message': str(e)}
            return JsonResponse(response_data, status=400)

    def get(self, request):
        robots = Robot.objects.all()
        robot_data = [{'serial': robot.serial, 'model': robot.model, 'version': robot.version, 'created': robot.created}
                      for robot in robots]
        return JsonResponse(robot_data, safe=False)


class DownloadReports(View):
    def get(self, request):
        # Извлекаем роботов за последнюю неделю за 7 полных дней от вчерашней даты
        today = datetime.today()
        end_of_last_week = (today - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)
        start_of_last_week = (end_of_last_week - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)

        robots = Robot.objects.filter(created__range=(start_of_last_week, end_of_last_week))

        # Создаем словарь для подсчета количества версий для каждой модели
        model_version_counts = defaultdict(lambda: defaultdict(int))

        for robot in robots:
            model_version_counts[robot.model][robot.version] += 1

        # Создаем Excel-файл и заполняем каждый лист моделями
        workbook = openpyxl.Workbook()
        for model, version_counts in model_version_counts.items():
            worksheet = workbook.create_sheet(title=model)
            worksheet.append(['Модель', 'Версия', 'Количество за неделю'])
            for version, count in version_counts.items():
                worksheet.append([model, version, count])

        # Удаляем первый автоматически созданный лист
        default_sheet = workbook.get_sheet_by_name('Sheet')
        workbook.remove(default_sheet)

        # Создаем байтовый объект для хранения файла Excel
        excel_file = BytesIO()
        workbook.save(excel_file)
        excel_file.seek(0)

        # Создаем имя файла
        file_name = f"robot_counts_{start_of_last_week.strftime('%Y-%m-%d')}_{end_of_last_week.strftime('%Y-%m-%d')}"

        # Создаем HTTP-ответ с содержимым файла Excel
        response = HttpResponse(excel_file.read(), content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{file_name}.xlsx"'

        return response
