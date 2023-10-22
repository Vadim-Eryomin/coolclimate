from .models import *


def add_data(req):
    categories = Categories.objects.all()

    is_admin = req.user.is_authenticated and req.user.is_superuser
    is_logged = req.user.is_authenticated

    cat = req.GET.get("active_category") or req.POST.get("active_category")
    cat = int(cat) if cat else 0

    q = req.GET.get("q") or req.POST.get("q")
    q = q if q else ""

    return {
        "all_categories": categories,
        "is_admin": is_admin,
        "is_logged": is_logged,
        "active_category": cat,
        "q": q,
    }
