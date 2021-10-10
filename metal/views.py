from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from metal.models import Value


class MetalPrice(APIView):

    def post(self, request):
        metal_names = request.data.get('Metal Name', None)
        date_from = request.data.get('Date-from', None)
        date_to = request.data.get('Date-To', None)
        frequency = request.data.get('Frequency', None)

        if not metal_names:
            return Response({'error': 'metal name missing'}, status=status.HTTP_400_BAD_REQUEST)

        if not date_from or not date_to:
            return Response({'error': 'from or to date missing'}, status=status.HTTP_400_BAD_REQUEST)

        result_set = []
        for metal_name in metal_names:
            data = Value.objects.filter(metal__metal_name=metal_name, updated_at__range=(date_from, date_to)).\
                order_by('updated_at')

            price_list = []
            for i in range(1, len(data)):
                different = data[i].updated_at - data[i - 1].updated_at
                hours = divmod(different.total_seconds(), 3600)[0]

                if frequency == 'hourly':
                    if hours >= 0:
                        price_list.append({"Price": data[i].value, "Updated at": str(data[i].updated_at)})
                elif frequency == 'daily':
                    if hours >= 24:
                        price_list.append({"Price": data[i].value, "Updated at": str(data[i].updated_at)})
                elif frequency == '7 days':
                    if hours >= 168:
                        price_list.append({"Price": data[i].value, "Updated at": str(data[i].updated_at)})
                else:
                    price_list.append({"Price": data[i].value, "Updated at": str(data[i].updated_at)})

            result_set.append({metal_name: {"Data": price_list}})

        return Response(result_set, status=status.HTTP_200_OK)
