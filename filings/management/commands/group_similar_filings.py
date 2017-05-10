import os

from django.core.management.base import BaseCommand, CommandError

from filings.models import Filing

from IPython import embed

from simhash_py import simhash as simhash_py

def filings_from_simhash(simhash):
    return Filing.objects.filter(simhash=simhash).all()

class Command(BaseCommand):
    help = 'Uses simhashes to group similar filings together'

    def add_arguments(self, parser):
        parser.add_argument('proceeding_name', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write("Starting group_similar_filings command...")

        proceeding_name = options['proceeding_name'][0]

        self.stdout.write("Grouping similar findings for for proceeding {}".format(proceeding_name))

        # find all filings in the docket that lack a simhash
        filings = Filing.objects.filter(proceeding=proceeding_name).all()[:50]

        counter = len(filings)

        hashes = []

        for filing in filings:
            if filing.simhash:
                hashes.append(int(filing.simhash))

        matches = simhash_py.find_all(hashes, 4, 3)

        groups = {}

        for match in matches:
            if not groups.get(match[0]):
                groups[match[0]] = []
            groups[match[0]].append(match[1])

        # for match in matches:
        #     if not groups.get(match[1]):
        #         groups[match[1]] = []
        #     groups[match[1]].append(match[0])

        clusters = []

        for key, value in groups.items():
            group = []
            group.append(key)
            for simhash in value:
                group.append(simhash)
            clusters.append(group)

        uniq_clusters = []
        for cluster in clusters:
            uniq_clusters.append(list(set(cluster)))

        clusters = uniq_clusters

        filings_clusters = []

        for cluster in clusters:
            filings_cluster = []
            for simhash in cluster:
                filings = filings_from_simhash(simhash)
                for filing in filings:
                    filings_cluster.append(filing)
            filings_clusters.append(filings_cluster)

        for filings_cluster in filings_clusters:
            print(len(filings_cluster))
            print(filings_cluster[0].pk)

        self.stdout.write("Finishing group_similar_filings command.")
