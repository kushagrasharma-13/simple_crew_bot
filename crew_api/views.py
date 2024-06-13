from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .main import generate_output_for_all_roles

@api_view(['POST'])
def get_crew_requirements(request):
    """Endpoint to get crew requirements based on user input."""
    try:
        crew_output = generate_output_for_all_roles(request.data)
        return Response({"crew": crew_output}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def health_check(request):
    return Response("OK", status=200)