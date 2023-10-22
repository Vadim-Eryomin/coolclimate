from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from random import choice


def admin_check(user: User):
    return user.is_superuser


# CRUD operations for Categories


@user_passes_test(admin_check, login_url="/login")
def get_all_categories(req):
    return render(
        req,
        "admin/categories/get_categories.html",
        {"categories": Categories.objects.values()},
    )


@user_passes_test(admin_check, login_url="/login")
def create_category(req):
    Categories.objects.create(title=req.POST.get("category")).save()
    return redirect("/categories")


@user_passes_test(admin_check, login_url="/login")
def edit_category(req):
    category = Categories.objects.get(id=req.POST.get("id"))
    category.title = req.POST.get("title")
    category.save()
    return redirect("/categories")


@user_passes_test(admin_check, login_url="/login")
def delete_category(req):
    Categories.objects.get(id=req.GET.get("id")).delete()
    return redirect("/categories")


@user_passes_test(admin_check, login_url="/login")
def choose_category_for_cards(req):
    categories = Categories.objects.values()
    for cat in categories:
        cat["count"] = Cards.objects.filter(category=cat["id"]).count()

    return render(
        req,
        "admin/cards/choose_category.html",
        {"categories": categories},
    )


@user_passes_test(admin_check, login_url="/login")
def get_all_cards(req, category_id):
    cards = Cards.objects.filter(category=category_id).values()
    return render(
        req, "admin/cards/all_cards.html", {"cards": cards, "category_id": category_id}
    )


@user_passes_test(admin_check, login_url="/login")
def new_card(req, category_id):
    category = Categories.objects.get(id=category_id)
    card = Cards.objects.create(title="Новая карточка товара", category=category)
    card.save()

    return redirect(f"/cards/{category_id}/{card.id}")


@user_passes_test(admin_check, login_url="/login")
def edit_card(req, category_id, card_id):
    card = Cards.objects.get(id=card_id)
    card.title = req.POST.get("title")
    card.description = req.POST.get("description")
    card.save()
    return redirect(f"/cards/{category_id}/{card.id}")


@user_passes_test(admin_check, login_url="/login")
def delete_card(req, category_id, card_id):
    Cards.objects.get(id=card_id).delete()
    return redirect(f"/cards/{category_id}")


@user_passes_test(admin_check, login_url="/login")
def check_card(req, category_id, card_id):
    card = Cards.objects.get(id=card_id)
    filter_values = []

    for filter in card.category.filters_set.values():
        filter_value = FilterValues.objects.filter(
            filters_id=filter["id"], card_id=card_id
        )
        if len(filter_value) == 0:
            filter_value = FilterValues.objects.create(
                filters_id=filter["id"],
                card_id=card.id,
                answer=("Новое значение" if filter["is_choice"] else 0),
            )
        else:
            filter_value = filter_value[0]

        filter_value.filter_title = filter["title"]
        filter_value.filter_type = filter["is_choice"]
        filter_value.save()
        filter_values.append(filter_value)

    return render(
        req,
        "admin/cards/card.html",
        {
            "card": card,
            "variants": card.cardvariants_set.all(),
            "images": card.cardimages_set.all(),
            "filters": filter_values,
        },
    )


@user_passes_test(admin_check, login_url="/login")
def new_variant(req, category_id, card_id):
    variant = CardVariants.objects.create(
        title=req.POST.get("title"),
        quantity=req.POST.get("quantity"),
        cost=req.POST.get("cost"),
        card_id=card_id,
    )

    variant.save()

    return redirect(
        f"/cards/{category_id}/{card_id}",
        {"card": variant.card},
    )


@user_passes_test(admin_check, login_url="/login")
def edit_variant(req, category_id, card_id):
    variant = CardVariants.objects.get(id=req.POST.get("id"))
    variant.title = req.POST.get("title")
    variant.quantity = req.POST.get("quantity")
    variant.cost = req.POST.get("cost")
    variant.save()

    return redirect(
        f"/cards/{category_id}/{card_id}",
        {"card": variant.card},
    )


@user_passes_test(admin_check, login_url="/login")
def delete_variant(req, category_id, card_id):
    CardVariants.objects.get(id=req.GET.get("id")).delete()
    return redirect(
        f"/cards/{category_id}/{card_id}",
        {"card": Cards.objects.get(id=card_id)},
    )


@user_passes_test(admin_check, login_url="/login")
def new_image(req, category_id, card_id):
    data = req.FILES.get("image")
    path = default_storage.save(data, ContentFile(data.read()))
    image = CardImages.objects.create(path=path, card_id=card_id)
    image.save()

    return redirect(
        f"/cards/{category_id}/{card_id}",
        {"card": Cards.objects.get(id=card_id)},
    )


@user_passes_test(admin_check, login_url="/login")
def delete_image(req, category_id, card_id):
    CardImages.objects.get(id=req.GET.get("id")).delete()

    return redirect(
        f"/cards/{category_id}/{card_id}",
        {"card": Cards.objects.get(id=card_id)},
    )


@user_passes_test(admin_check, login_url="/login")
def edit_card_filter_value(req, category_id, card_id):
    keys = [x for x in req.POST if x != "csrfmiddlewaretoken"]

    for key in keys:
        value = req.POST.get(key)
        filter_value = FilterValues.objects.get(id=key)
        filter_value.answer = value
        filter_value.save(update_fields=["answer"])

    return redirect(
        f"/cards/{category_id}/{card_id}",
        {"card": Cards.objects.get(id=card_id)},
    )


@user_passes_test(admin_check, login_url="/login")
def choose_category_for_filters(req):
    categories = Categories.objects.values()
    for cat in categories:
        cat["cards"] = Cards.objects.filter(category=cat["id"]).count()
        cat["filters"] = Filters.objects.filter(category=cat["id"]).count()

    return render(
        req,
        "admin/filters/choose_category.html",
        {"categories": categories},
    )


@user_passes_test(admin_check, login_url="/login")
def get_all_filters(req, category_id):
    filters = Filters.objects.filter(category=category_id).values()
    return render(
        req,
        "admin/filters/all_filters.html",
        {"filters": filters, "category_id": category_id},
    )


@user_passes_test(admin_check, login_url="/login")
def new_filter(req, category_id):
    category = Categories.objects.get(id=category_id)
    filter = Filters.objects.create(title="Новый фильтр", category=category)
    filter.save()

    return redirect(f"/filters/{category_id}/{filter.id}")


@user_passes_test(admin_check, login_url="/login")
def check_filter(req, category_id, filter_id):
    filter = Filters.objects.get(id=filter_id)
    return render(
        req,
        "admin/filters/filter.html",
        {"filter": filter},
    )


@user_passes_test(admin_check, login_url="/login")
def edit_filter(req, category_id, filter_id):
    filter = Filters.objects.get(id=filter_id)
    filter.title = req.POST.get("title")
    filter.is_choice = req.POST.get("type") == "true"
    filter.save()
    return redirect(f"/filters/{category_id}/{filter.id}")


@user_passes_test(admin_check, login_url="/login")
def delete_filter(req, category_id, filter_id):
    Filters.objects.get(id=filter_id).delete()
    return redirect(f"/filters/{category_id}")


def intersect(a, b):
    return [x for x in a if x in b]


def index(req):
    cards = []

    if req.method == "GET":
        active_category = req.GET.get("active_category")
        q = req.GET.get("q") if req.GET.get("q") is not None else ""
    else:
        active_category = req.POST.get("active_category")
        q = req.POST.get("q") if req.POST.get("q") is not None else ""

        used_filters = [int(x) for x in req.POST if x.isnumeric()]
        used_filter_values = {x: req.POST.getlist(str(x)) for x in used_filters}

    cards = Cards.objects.all()
    if q:
        cards = cards.filter(title__contains=q)
    if active_category:
        cards = cards.filter(category_id=active_category)

    for card in cards:
        images = card.cardimages_set.values()
        if images:
            card.image = images[0]["path"]
        else:
            card.image = "default.png"

    if req.method == "POST":
        need_cards = [card.id for card in cards]
        for used_filter in used_filters:
            if Filters.objects.get(id=used_filter).is_choice:
                need_cards = intersect(
                    need_cards,
                    [
                        x.card.id
                        for x in FilterValues.objects.filter(
                            filters=used_filter,
                            id__in=list(map(int, used_filter_values[used_filter])),
                        )
                    ],
                )
            else:
                need_cards = intersect(
                    need_cards,
                    [
                        x.card.id
                        for x in FilterValues.objects.filter(
                            filters=used_filter,
                            answer__gte=int(used_filter_values[used_filter][0]),
                            answer__lte=int(used_filter_values[used_filter][1]),
                        )
                    ],
                )
        cards = [card for card in cards if card.id in need_cards]
    filters = []
    if active_category:
        filters = Filters.objects.filter(category_id=active_category)
        for _filter in filters:
            _filter.filtervalues = FilterValues.objects.filter(filters=_filter).values()
            if not _filter.is_choice:
                min_value = 99999999999999
                max_value = 0

                for value in _filter.filtervalues:
                    answer = value["answer"]
                    if not answer.isnumeric():
                        continue
                    answer = int(answer)

                    min_value = min(min_value, answer)
                    max_value = max(max_value, answer)

                _filter.min = min_value
                _filter.max = max_value

        return render(
            req, "client/filters_page.html", {"cards": cards, "filters": filters}
        )

    return render(req, "client/main.html", {"cards": cards})


def card_data(req, card_id):
    card = Cards.objects.get(id=card_id)
    images = card.cardimages_set.all()
    variants = card.cardvariants_set.all()
    filters = card.filtervalues_set.all()
    if not images:
        images = ["default.png"]

    cart = req.session.get("cart", [])
    for variant in variants:
        variant.in_cart = str(variant.id) in cart

    for _filter in filters:
        _filter.title = _filter.filters.title

    return render(
        req,
        "client/card_data.html",
        {"card": card, "images": images, "filters": filters, "variants": variants},
    )


def add_to_card(req):
    variant_id = req.POST.get("variant")
    variant = CardVariants.objects.get(id=variant_id)

    if not req.session.get("cart"):
        req.session["cart"] = []
    req.session["cart"] += [variant_id]

    return redirect(f"/card/{variant.card.id}")


def cart(req):
    variants = []
    for variant_id in list(set(req.session.get("cart", []))):
        variant = CardVariants.objects.get(id=variant_id)
        variant.card_title = variant.card.title

        variant.image = variant.card.cardimages_set.all()[0]
        variant.image = variant.image.path if variant.image else "default.png"

        variants.append(variant)

    return render(req, "client/cart.html", {"variants": variants})


@login_required(login_url="/login")
def delete_cart(req):
    variant = req.GET.get("variant")
    req.session["cart"] = [x for x in req.session["cart"] if x != variant]
    return redirect("/cart")


def register_page(req):
    return render(req, "client/register.html")


def register_account(req):
    username = req.POST.get("username")
    password1 = req.POST.get("password1")
    password2 = req.POST.get("password2")

    if username is None or password1 is None or password2 is None:
        return redirect("/register")

    if password1 != password2:
        return redirect("/register")

    user = User.objects.create_user(username=username, password=password1)
    user.save()
    login(req, user)
    return redirect("/fill_profile")


@login_required(login_url="/login")
def fill_account(req):
    return render(req, "client/fill_profile.html")


@login_required(login_url="/login")
def create_account(req):
    user = req.user
    profile = Profiles.objects.create(
        fio=req.POST.get("fio"),
        street=req.POST.get("street"),
        house=req.POST.get("house"),
        corps=req.POST.get("corps"),
        flat=req.POST.get("flat"),
        phone=req.POST.get("phone"),
        user=user,
    )
    profile.save()
    return redirect("/")


def login_page(req):
    return render(req, "client/login.html")


def login_account(req):
    username = req.POST.get("username")
    password = req.POST.get("password")
    print(username, password)

    user = authenticate(username=username, password=password)
    if user is None:
        return redirect("/login")

    login(req, user)
    return redirect("/")


@login_required(login_url="/login")
def logout_account(req):
    logout(req)
    return redirect("/")


@login_required(login_url="/login")
def check_order_correctness(req):
    variants = req.POST.getlist("variant")
    quantities = req.POST.getlist("quantity")
    computed_variants = []

    total = 0
    has_all = True

    for variant, quantity in zip(variants, quantities):
        variant = CardVariants.objects.get(id=variant)
        variant.card_title = variant.card.title
        variant.buy_quantity = quantity

        images_set = variant.card.cardimages_set.all()
        variant.image = images_set[0].path if images_set else "default.png"
        computed_variants.append(variant)

        subtotal = round(int(quantity) * float(variant.cost), 2)
        variant.total = subtotal
        total += subtotal
        if variant.quantity <= 0:
            has_all = False

    total = round(total, 2)

    profile = []
    if hasattr(req.user, "profiles"):
        profile = req.user.profiles

    return render(
        req,
        "client/create_order.html",
        {
            "variants": computed_variants,
            "total": total,
            "has_all": has_all,
            "profile": profile,
        },
    )


@login_required(login_url="/login")
def make_order(req):
    variants = req.POST.getlist("variant")
    quantities = req.POST.getlist("quantity")

    fio = req.POST.get("fio")
    street = req.POST.get("street")
    house = req.POST.get("house")
    corps = req.POST.get("corps")
    room = req.POST.get("room")
    phone = req.POST.get("phone")

    comment = req.POST.get("comment")
    delivery = req.POST.get("delivery")

    track = "climate-"
    elements = "0123456789abcdefghijklmnopqrstuvwxyz"
    for i in range(10):
        track += choice(elements)

    order = Orders.objects.create(
        comment=comment,
        is_delivery=delivery is not None,
        fio=fio,
        street=street,
        house=house if house else "",
        corps=corps if corps else "",
        room=room if room else "",
        phone=phone,
        track=track,
        user=req.user,
        status="Ожидает рассмотрения",
    )
    order.save()

    for variant, quantity in zip(variants, quantities):
        variant = CardVariants.objects.get(id=variant)
        OrderEntries.objects.create(
            quantity=quantity, variant=variant, buy_cost=variant.cost, order=order
        ).save()

    req.session["cart"] = []

    return render(req, "client/order_created.html", {"track": track})


def check_order(req):
    order = req.GET.get("query")
    entries = []
    total = 0
    has_all = True

    if order and Orders.objects.filter(track=order).count() > 0:
        order = Orders.objects.get(track=order)
        print(order.is_delivery)
        entries = []
        total = 0

        for entry in order.orderentries_set.all():
            variant = entry.variant
            card_title = variant.card.title

            card_images = variant.card.cardimages_set.all()
            card_image = card_images[0] if card_images else "default.png"

            entry.variant = variant
            entry.card_title = card_title
            entry.card_image = card_image
            entry.total = entry.quantity * entry.buy_cost

            if variant.quantity < entry.quantity:
                has_all = False

            total += entry.total
            entries.append(entry)

    return render(
        req,
        "client/check_order.html",
        {
            "order": order,
            "entries": entries,
            "total": round(total, 2),
            "has_all": has_all,
        },
    )


@user_passes_test(admin_check, login_url="/login")
def all_orders_by_statuses(req):
    order_groups = {}
    for order in Orders.objects.all():
        if not order.status:
            order_groups["Неопределенные"] = order_groups.get("Неопределенные", 0) + 1
        else:
            order_groups[order.status] = order_groups.get(order.status, 0) + 1

    return render(
        req, "admin/orders/orders_by_statuses.html", {"status_groups": order_groups}
    )


@user_passes_test(admin_check, login_url="/login")
def status_orders(req, title):
    return render(
        req,
        "admin/orders/status_orders.html",
        {
            "orders": Orders.objects.filter(
                status=(title if title != "Неопределенные" else "")
            ),
            "status": title,
        },
    )


@user_passes_test(admin_check, login_url="/login")
def admin_track_order(req, track):
    order = track
    entries = []
    total = 0
    has_all = True
    statuses = list(set([order.status for order in Orders.objects.all()]))

    if order and Orders.objects.filter(track=order).count() > 0:
        order = Orders.objects.get(track=order)
        entries = []
        total = 0

        for entry in order.orderentries_set.all():
            variant = entry.variant
            card_title = variant.card.title

            card_images = variant.card.cardimages_set.all()
            card_image = card_images[0] if card_images else "default.png"

            entry.variant = variant
            entry.card_title = card_title
            entry.card_image = card_image
            entry.total = entry.quantity * entry.buy_cost

            if variant.quantity < entry.quantity:
                has_all = False

            total += entry.total
            entries.append(entry)

    return render(
        req,
        "admin/orders/track_order.html",
        {
            "order": order,
            "entries": entries,
            "total": round(total, 2),
            "has_all": has_all,
            "statuses": statuses,
        },
    )


@user_passes_test(admin_check, login_url="/login")
def change_order_status(req, track):
    order = Orders.objects.get(track=track)
    order.status = req.POST.get("status")
    order.save()

    return redirect(f"/orders/track/{track}")


def filter_cards(req):
    return render(req, "client/categorized.html")


@login_required(login_url="/login")
def show_profile(req):
    profile = []
    if hasattr(req.user, "profiles"):
        profile = req.user.profiles
    orders = req.user.orders_set.all()

    return render(req, "client/profile.html", {"profile": profile, "orders": orders})


@login_required(login_url="/login")
def edit_profile(req):
    user = req.user
    if not hasattr(req.user, "profiles"):
        profile = Profiles.objects.create(
            fio=req.POST.get("fio"),
            street=req.POST.get("street"),
            house=req.POST.get("house"),
            corps=req.POST.get("corps"),
            flat=req.POST.get("flat"),
            phone=req.POST.get("phone"),
            user=user,
        )
    else:
        profile = user.profiles
        profile.fio = req.POST.get("fio")
        profile.street = req.POST.get("street")
        profile.house = req.POST.get("house")
        profile.corps = req.POST.get("corps")
        profile.flat = req.POST.get("flat")
        profile.phone = req.POST.get("phone")

    profile.save()
    return redirect("/profile")


@login_required(login_url="/login")
def change_password(req):
    old_password = req.POST.get("old_password")
    new_password = req.POST.get("new_password")
    repeat_password = req.POST.get("repeat_password")

    if not req.user.check_password(old_password) or new_password != repeat_password:
        return redirect("/profile?error=true")

    req.user.set_password(new_password)
    return redirect("/profile?success=true")


def about(req):
    return render(req, "client/about.html")


@user_passes_test(admin_check, login_url="/login")
def get_all_certificates(req):
    return render(
        req,
        "admin/certificates/all_certificates.html",
        {"certificates": Certificates.objects.all()},
    )


@user_passes_test(admin_check, login_url="/login")
def get_certificate(req, cert_id):
    return render(
        req,
        "admin/certificates/certificate.html",
        {"certificate": Certificates.objects.get(id=cert_id)},
    )
