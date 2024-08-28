from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from .ml_model import train_model, predict, get_metrics

class TrainModelView(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Trigger model training process
            train_model()
            return Response({"message": "Model training started"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PredictView(views.APIView):
    def post(self, request, *args, **kwargs):
        input_data = request.data.get('input')
        if input_data is None:
            return Response({"error": "No input data provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            prediction = predict(input_data)
            return Response({"prediction": prediction}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MetricsView(views.APIView):
    def get(self, request, *args, **kwargs):
        try:
            metrics = get_metrics()
            return Response({"metrics": metrics}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
