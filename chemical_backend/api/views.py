from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from .models import Dataset
from .serializers import DatasetSerializer
from .utils import compute_summary
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import permissions
import pandas as pd

import pandas as pd

def analyze_csv(file_obj):
    df = pd.read_csv(file_obj)

    # Normalize column names (VERY IMPORTANT)
    df.columns = [c.strip().lower() for c in df.columns]

    required_columns = {"type", "flowrate", "pressure", "temperature"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"CSV must contain columns: {required_columns}. Found: {df.columns.tolist()}"
        )

    summary = {
        "total_count": len(df),
        "type_distribution": df["type"].value_counts().to_dict(),
        "statistics": {
            "flowrate": {
                "avg": float(df["flowrate"].mean()),
                "min": float(df["flowrate"].min()),
                "max": float(df["flowrate"].max()),
            },
            "pressure": {
                "avg": float(df["pressure"].mean()),
                "min": float(df["pressure"].min()),
                "max": float(df["pressure"].max()),
            },
            "temperature": {
                "avg": float(df["temperature"].mean()),
                "min": float(df["temperature"].min()),
                "max": float(df["temperature"].max()),
            },
        },
    }

    return summary



class UploadCSVView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        file_obj = request.FILES.get("file")

        if not file_obj:
            return Response({"error": "File required"}, status=400)

        if not file_obj.name.lower().endswith(".csv"):
            return Response({"error": "Only CSV files allowed"}, status=400)

        # ---- ANALYZE CSV ----
        try:
            summary = analyze_csv(file_obj)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        # ---- LIMIT HISTORY TO LAST 5 ----
        existing = Dataset.objects.filter(user=request.user).order_by("created_at")

        if existing.count() >= 5:
            oldest = existing.first()
            oldest.delete()

        # ---- SAVE DATASET ----
        dataset = Dataset.objects.create(
            user=request.user,
            name=file_obj.name,
            file=file_obj,
            summary_json=summary,
        )

        return Response({
            "id": dataset.id,
            "summary": summary
        })


class DatasetSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(
                id=pk,
                user=request.user
            )
        except Dataset.DoesNotExist:
            return Response(
                {"error": "Dataset not found"},
                status=404
            )

        return Response(dataset.summary_json)




class DatasetHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        datasets = (
            Dataset.objects
            .filter(user=request.user)
            .order_by("-created_at")[:5]
        )

        data = [
            {
                "id": d.id,
                "name": d.name,
                "created_at": d.created_at.strftime("%Y-%m-%d %H:%M")
            }
            for d in datasets
        ]

        return Response(data)



from django.http import HttpResponse
import tempfile
from .pdf_utils import build_pdf_report
from .models import Dataset
from rest_framework.views import APIView
from rest_framework import permissions


from rest_framework.views import APIView
from rest_framework import permissions
from django.http import HttpResponse
import tempfile

from .models import Dataset
from .pdf_utils import build_pdf_report


class DatasetReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        dataset = Dataset.objects.get(id=pk, user=request.user)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            build_pdf_report(
                file_path=tmp.name,
                summary=dataset.summary_json,
                user=request.user,
            )
            tmp.seek(0)
            pdf_data = tmp.read()

        response = HttpResponse(pdf_data, content_type="application/pdf")
        response["Content-Disposition"] = (
            "attachment; filename=dataset_report.pdf"
        )
        return response




from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class LoginView(APIView):
    permission_classes = []  # allow anyone to call

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import permissions


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=400
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "User already exists"},
                status=400
            )

        # 🔴 CORRECT WAY TO CREATE USER
        user = User.objects.create_user(
            username=username,
            password=password
        )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "username": user.username
        })

