# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.
from django.core.management.base import BaseCommand
from atmo.clusters.jobs import update_clusters_info


class Command(BaseCommand):
    help = 'Go through active clusters and update their status'

    def handle(self, *args, **options):
        update_clusters_info()
