from datetime import datetime

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View
from .models import Robot
import json


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
