from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, F
from django.utils.timezone import datetime

from metal.models import Metal, Value


class MetalPrice(APIView):

    def post(self, request):
        metal_names = request.data.get('Metal Name', None)
        date_from = request.data.get('Date-from', None)
        date_to = request.data.get('Date-To', None)
        frequency = request.data.get('Frequency', None)

        result_set = []
        for metal_name in metal_names:
            data = Value.objects.filter(metal__metal_name=metal_name, created_at__range=(date_from, date_to))
            price_list = []
            for d in data:
                price_list.append({"Price": d.value, "Updated at": str(d.updated_at)})

            result_set.append({metal_name: price_list})

        print(result_set)

        return Response()
