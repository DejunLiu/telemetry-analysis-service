import logging
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .clusters.forms import NewClusterForm, EditClusterForm, DeleteClusterForm
from .clusters.models import Cluster
from .jobs.forms import NewSparkJobForm, EditSparkJobForm, DeleteSparkJobForm
from .jobs.models import SparkJob


logger = logging.getLogger("django")


@login_required
def dashboard(request):
    username = request.user.email.split("@")[0]
    clusters = (Cluster.objects.filter(created_by=request.user)
                               .filter(end_date__gt=timezone.now() - timedelta(days=1))
                               .order_by("start_date"))
    jobs = SparkJob.objects.filter(created_by=request.user).order_by("start_date")
    context = {
        "active_clusters": clusters,
        "new_cluster_form": NewClusterForm(request.user, initial={
            "identifier": "{}-telemetry-analysis".format(username),
            "size": 1,
        }),
        "edit_cluster_form": EditClusterForm(request.user),
        "delete_cluster_form": DeleteClusterForm(request.user),

        "user_spark_jobs": jobs,
        "new_spark_job_form": NewSparkJobForm(request.user, initial={
            "identifier": "{}-telemetry-scheduled-task".format(username),
            "size": 1,
            "interval_in_hours": 24 * 7,
            "job_timeout": 24,
            "start_date": datetime.now(),
        }),
        "edit_spark_job_form": EditSparkJobForm(request.user),
        "delete_spark_job_form": DeleteSparkJobForm(request.user),
    }
    return render(request, 'atmo/dashboard.html', context=context)
