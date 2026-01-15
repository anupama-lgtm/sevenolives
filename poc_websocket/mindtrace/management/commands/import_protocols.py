import os
import glob
import json
from typing import Any, Dict, List, Tuple

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from mindtrace.models import Assessment, Protocol, ProtocolAssessment


class Command(BaseCommand):
    help = (
        "Import assessment and protocol definitions into the MindTrace tables.\n"
        "- Use --assessments-file to load AllAssessments.json (creates Assessments).\n"
        "- Optionally use --protocols-path to scan for protocol JSONs (creates Protocol + ordering).\n"
        "Run without --apply for a dry run."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--assessments-file",
            required=False,
            help="Path to AllAssessments.json (contains array under 'assessments')",
        )
        parser.add_argument(
            "--protocols-path",
            required=False,
            help="Directory containing protocol JSONs (each file defines a protocol)",
        )
        parser.add_argument(
            "--glob",
            default="*.json",
            help="Glob to select protocol JSON files within --protocols-path (default: *.json)",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Apply changes to the database (omit for dry run)",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Verbose output",
        )

    def handle(self, *args, **options):
        afile = options.get("assessments_file") or options.get("--assessments-file")
        protocols_path = options.get("protocols_path")
        pattern = options.get("glob") or "*.json"
        apply_changes = options.get("apply", False)
        verbose = options.get("verbose", False)

        created_counts = {"assessments": 0, "protocols": 0, "links": 0}

        # Load assessments if a file is provided
        if afile:
            if not os.path.isfile(afile):
                raise CommandError(f"Assessments file not found: {afile}")

            with open(afile, "r", encoding="utf-8") as f:
                content = json.load(f)
            assessments = content.get("assessments")
            if not isinstance(assessments, list):
                raise CommandError("Invalid AllAssessments.json: missing 'assessments' array")

            if apply_changes:
                with transaction.atomic():
                    for item in assessments:
                        name = str(item.get("name") or "").strip()
                        if not name:
                            continue
                        psyexp = str(item.get("psyexp") or "").strip()
                        obj, created = Assessment.objects.get_or_create(
                            name=name,
                            defaults={"psyexp": psyexp},
                        )
                        if created:
                            created_counts["assessments"] += 1
                        else:
                            if psyexp and obj.psyexp != psyexp:
                                Assessment.objects.filter(id=obj.id).update(psyexp=psyexp)
                if verbose:
                    self.stdout.write(self.style.SUCCESS(f"Processed {len(assessments)} assessments from {afile}"))
            else:
                self.stdout.write(self.style.WARNING(f"Dry run: would process {len(assessments)} assessments from {afile}"))

        # Load protocols if requested
        if protocols_path and os.path.isdir(protocols_path):
            files = [
                p for p in glob.glob(os.path.join(protocols_path, pattern))
                if os.path.isfile(p)
            ]
            # Skip the AllAssessments.json itself
            if afile:
                files = [p for p in files if os.path.abspath(p) != os.path.abspath(afile)]

            if verbose:
                self.stdout.write(self.style.MIGRATE_HEADING(f"Scanning {len(files)} protocol file(s)"))

            for fp in files:
                try:
                    with open(fp, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception as exc:
                    if verbose:
                        self.stderr.write(self.style.ERROR(f"Skip {fp}: {exc}"))
                    continue

                proto_name, items = self._extract_protocol(data)
                if not proto_name:
                    # infer from filename
                    proto_name = os.path.splitext(os.path.basename(fp))[0]
                if not proto_name or not items:
                    continue

                if apply_changes:
                    with transaction.atomic():
                        protocol, p_created = Protocol.objects.get_or_create(name=proto_name)
                        if p_created:
                            created_counts["protocols"] += 1
                        # Clear existing ordering for idempotency
                        ProtocolAssessment.objects.filter(protocol=protocol).delete()

                        for order, item in enumerate(items):
                            aname = (item.get("name") or "").strip()
                            psyexp = (item.get("psyexp") or "").strip()
                            if not aname:
                                continue
                            assessment, a_created = Assessment.objects.get_or_create(
                                name=aname,
                                defaults={"psyexp": psyexp},
                            )
                            if a_created:
                                created_counts["assessments"] += 1
                            elif psyexp and assessment.psyexp != psyexp:
                                Assessment.objects.filter(id=assessment.id).update(psyexp=psyexp)
                            ProtocolAssessment.objects.create(
                                protocol=protocol,
                                assessment=assessment,
                                order=order,
                            )
                            created_counts["links"] += 1
                else:
                    if verbose:
                        self.stdout.write(f"[DRY] Protocol {proto_name}: {len(items)} assessments")

        self.stdout.write(self.style.SUCCESS(f"Done. Created: {created_counts}"))

    # ---- helpers ----

    def _extract_protocol(self, data: Dict[str, Any]) -> Tuple[str | None, List[Dict[str, str]]]:
        """Best-effort parse of a protocol JSON file.
        Accepts structures like:
        - { "name": "MyProtocol", "assessments": ["A", "B", ...] }
        - { "name": "MyProtocol", "assessments": [{"name": "A", "psyexp": "..."}, {"name": "B"}] }
        - { "protocol": "MyProtocol", "items": [ ... names ... ] }
        Returns (protocol_name, list of {name, psyexp?}).
        """
        name = None
        items: List[Dict[str, str]] = []

        if isinstance(data, dict):
            name = data.get("name") or data.get("protocol")
            assessments = data.get("assessments") or data.get("items")
            if isinstance(assessments, list):
                for it in assessments:
                    if isinstance(it, str):
                        n = it.strip()
                        if n:
                            items.append({"name": n})
                    elif isinstance(it, dict):
                        n = it.get("name") or it.get("assessment")
                        if n:
                            items.append({
                                "name": str(n).strip(),
                                "psyexp": str(it.get("psyexp") or "").strip(),
                            })
        return (str(name).strip() if name else None, [i for i in items if i.get("name")])
