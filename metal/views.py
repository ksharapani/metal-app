import pandas as pd
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
            price_list = []
            data = Value.objects.values('updated_at', 'value').\
                filter(metal__metal_name=metal_name, updated_at__range=(date_from, date_to)). \
                order_by('updated_at')
            if frequency == 'hourly':
                for d in data:
                    price_list.append({"Price": d.value, "Updated at": str(d.updated_at)})

            elif frequency == 'daily':
                if data:
                    data_frame = pd.DataFrame(list(data))
                    mean = data_frame.groupby([data_frame['updated_at'].dt.date])['value'].mean()

                    for index, value in mean.items():
                        price_list.append({"Price": value, "Updated at": index})

            elif frequency == '7 days':
                if data:
                    data_frame = pd.DataFrame(list(data))
                    mean = data_frame.resample('W-Mon', on='updated_at').mean()

                    for index, value in mean.iterrows():
                        price_list.append({"Price": value[0], "Updated at": index})

            result_set.append({metal_name: {"Data": price_list}})

        return Response(result_set, status=status.HTTP_200_OK)
