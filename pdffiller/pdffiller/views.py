import os
from pathlib import Path
from datetime import timedelta, datetime
import sys
import threading
import logging

from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404

from .forms import NewClientForm
from .doc_filler import fill_pdf_by_coordinates, coordinates, name_pdf_template_map

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def download_pdf(request, company_name, template_name):
    file_path = os.path.join(settings.MEDIA_ROOT, company_name, template_name)

    if not os.path.exists(file_path):
        raise Http404("File not found")

    try:
        return FileResponse(
            open(file_path, "rb"),
            content_type="application/pdf",
            as_attachment=True,
            filename=template_name,
        )
    except Exception as e:
        raise Http404(f"Error downloading file: {str(e)}")


def delete_old_files(file_paths):
    current_time = timezone.now()
    for file_path in file_paths:
        if file_path.exists():
            file_mod_time = timezone.make_aware(
                datetime.fromtimestamp(file_path.stat().st_mtime)
            )
            file_age = current_time - file_mod_time
            logging.info(
                f"File: {file_path}, Last Modified: {file_mod_time}, Age: {file_age}"
            )

            # Check if the file is older than 1 minute
            if file_age > timedelta(minutes=10):
                try:
                    os.remove(file_path)
                    logging.info(f"Deleted old file: {file_path}")
                except Exception as e:
                    logging.error(f"Error deleting file {file_path}: {e}")
            else:
                logging.info(f"File not old enough to delete: {file_path}")
        else:
            logging.warning(f"File does not exist: {file_path}")


def index(request):
    return render(request, "pdffiller/index.html")


@login_required
def create_client(request):
    username = request.user.username

    if request.method == "POST":
        form = NewClientForm(request.POST)
        if form.is_valid():
            form_data = {
                "first_name": request.POST.get("first_name"),
                "last_name": request.POST.get("last_name"),
                "dob": request.POST.get("dob"),
                "ssn": request.POST.get("ssn"),
                "phone": request.POST.get("phone"),
                "email": request.POST.get("email"),
                "address": request.POST.get("address"),
                "city": request.POST.get("city"),
                "state": request.POST.get("state"),
                "zip_code": request.POST.get("zip_code"),
                "company_name": request.POST.get("company_name"),
                "company_address": request.POST.get("company_address"),
                "company_city": request.POST.get("company_city"),
                "company_state": request.POST.get("company_state"),
                "company_zip": request.POST.get("company_zip"),
                "ein": request.POST.get("ein"),
                "date_of_incorporation": request.POST.get("date_of_incorporation"),
            }

            templates_and_links = []
            generated_files = []

            for name, template in name_pdf_template_map.items():
                if (
                    username != "CFSadmin"
                    and (template == "CFS.pdf" or template == "GeorgeFinance.pdf")
                ) or (username == "CFSadmin" and template == "GandR.pdf"):
                    continue

                name_coordinate = coordinates.get(name, None)
                if not name_coordinate:
                    continue

                path_to_template = settings.BASE_DIR / "applications" / template
                if not path_to_template.exists():
                    continue

                path_to_save_dir = Path(settings.MEDIA_ROOT) / form_data["company_name"]
                path_to_save_dir.mkdir(exist_ok=True, parents=True)

                font_size = 8
                if template == "PeterBrakner.pdf":
                    font_size = 6

                fill_pdf_by_coordinates(
                    path_to_template,
                    path_to_save_dir / template,
                    form_data,
                    name_coordinate,
                    font_size,
                )

                download_link = os.path.join(
                    settings.MEDIA_URL, form_data["company_name"], template
                )
                templates_and_links.append((template, download_link))

                generated_files.append(path_to_save_dir / template)

            def delete_files_later():
                threading.Timer(600, delete_old_files, [generated_files]).start()

            delete_files_later()

            logging.info(templates_and_links)

            return render(
                request,
                "pdffiller/success.html",
                {"templates_and_links": templates_and_links, "form_data": form_data},
            )
    else:
        form = NewClientForm()
    return render(request, "pdffiller/create_client.html", {"form": form})
