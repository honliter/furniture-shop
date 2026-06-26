from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CheckoutForm, FurnitureForm
from .models import Furniture, Category


STARTER_CATEGORIES = ['Дивани', 'Крісла', 'Столи', 'Ліжка', 'Шафи', 'Декор', 'Освітлення', 'Для офісу']

STARTER_FURNITURE = [
    ('Диван Oslo', 'Мʼякий тримісний диван у скандинавському стилі з міцним деревʼяним каркасом.', 18900, 'Дивани', '🛋️', 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=900&q=80'),
    ('Кутовий диван Verona', 'Просторий кутовий диван для сімейної вітальні з нішою для зберігання.', 27600, 'Дивани', '🛋️', 'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&w=900&q=80'),
    ('Крісло Luna', 'Затишне крісло для читання з високою спинкою та мʼякою оббивкою.', 7400, 'Крісла', '🪑', 'https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?auto=format&fit=crop&w=900&q=80'),
    ('Крісло-гойдалка Relax', 'Стильне крісло-гойдалка для спальні, балкона або лаунж-зони.', 6900, 'Крісла', '🪑', 'https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?auto=format&fit=crop&w=900&q=80'),
    ('Обідній стіл Milan', 'Деревʼяний обідній стіл на шість персон із натуральною текстурою дуба.', 12800, 'Столи', '🍽️', 'https://images.unsplash.com/photo-1577140917170-285929fb55b7?auto=format&fit=crop&w=900&q=80'),
    ('Журнальний столик Nord', 'Компактний журнальний столик із мінімалістичними металевими ніжками.', 4200, 'Столи', '☕', 'https://images.unsplash.com/photo-1532372320978-9d3d0f39bb4b?auto=format&fit=crop&w=900&q=80'),
    ('Ліжко Dream 160', 'Двоспальне ліжко з мʼяким узголівʼям і ортопедичною основою.', 16400, 'Ліжка', '🛏️', 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80'),
    ('Ліжко Soft Cloud', 'Преміальне ліжко з текстильною оббивкою та підйомним механізмом.', 21900, 'Ліжка', '🛏️', 'https://images.unsplash.com/photo-1617325247661-675ab4b64ae2?auto=format&fit=crop&w=900&q=80'),
    ('Шафа Classic', 'Містка тридверна шафа для одягу з полицями та штангою.', 14200, 'Шафи', '🚪', 'https://images.unsplash.com/photo-1595428774223-ef52624120d2?auto=format&fit=crop&w=900&q=80'),
    ('Комод Terra', 'Комод із чотирма шухлядами для спальні або передпокою.', 8800, 'Шафи', '🗄️', 'https://images.unsplash.com/photo-1594026112284-02bb6f3352fe?auto=format&fit=crop&w=900&q=80'),
    ('Торшер Amber', 'Теплий торшер для вечірнього освітлення вітальні.', 3100, 'Освітлення', '💡', 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80'),
    ('Настільна лампа Focus', 'Лаконічна лампа для робочого столу з регульованим нахилом.', 1900, 'Освітлення', '💡', 'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=900&q=80'),
    ('Дзеркало Aurora', 'Велике настінне дзеркало в тонкій декоративній рамі.', 3600, 'Декор', '🪞', 'https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=900&q=80'),
    ('Килим Sand', 'Мʼякий килим нейтрального відтінку для зонування простору.', 5200, 'Декор', '🧶', 'https://images.unsplash.com/photo-1600166898405-da9535204843?auto=format&fit=crop&w=900&q=80'),
    ('Офісний стіл Pro', 'Практичний письмовий стіл із кабель-менеджментом.', 9700, 'Для офісу', '🖥️', 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?auto=format&fit=crop&w=900&q=80'),
    ('Ергономічне крісло Work', 'Регульоване офісне крісло для комфортної роботи вдома.', 11600, 'Для офісу', '💺', 'https://images.unsplash.com/photo-1580480055273-228ff5388ef8?auto=format&fit=crop&w=900&q=80'),
]


def seed_catalog_if_empty():
    for category_name in STARTER_CATEGORIES:
        Category.objects.get_or_create(name=category_name)

    if Furniture.objects.count() >= 12:
        return

    for title, description, price, category_name, emoji, image_url in STARTER_FURNITURE:
        category = Category.objects.get(name=category_name)
        Furniture.objects.get_or_create(
            title=title,
            defaults={
                'description': description,
                'price': price,
                'category': category,
                'emoji': emoji,
                'image_url': image_url,
            }
        )


def cart_count(request):
    cart = request.session.get('cart', {})
    return sum(cart.values())


def home(request):
    seed_catalog_if_empty()
    category_id = request.GET.get('category')
    items = Furniture.objects.select_related('category').all().order_by('category__name', 'title')
    if category_id:
        items = items.filter(category_id=category_id)
    categories = Category.objects.all().order_by('name')
    return render(request, 'store/home.html', {
        'items': items,
        'cart_count': cart_count(request),
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Ласкаво просимо, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Невірний логін або пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form, 'cart_count': cart_count(request)})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Акаунт створено! Ласкаво просимо, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Помилка реєстрації. Перевірте дані.')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form, 'cart_count': cart_count(request)})


def logout_view(request):
    logout(request)
    messages.success(request, 'Ви успішно вийшли з акаунту.')
    return redirect('login')


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Furniture, pk=pk)
    cart = request.session.get('cart', {})
    key = str(pk)
    cart[key] = cart.get(key, 0) + 1
    request.session['cart'] = cart
    messages.success(request, f'"{item.title}" додано до кошика!')
    return redirect('home')


@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for pk, qty in cart.items():
        try:
            item = Furniture.objects.get(pk=int(pk))
            subtotal = item.price * qty
            total += subtotal
            items.append({'item': item, 'qty': qty, 'subtotal': subtotal})
        except Furniture.DoesNotExist:
            pass
    return render(request, 'store/cart.html', {'cart_items': items, 'total': total, 'cart_count': cart_count(request)})


@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Кошик порожній. Додайте товари перед оформленням.')
        return redirect('home')

    items = []
    total = 0
    for pk, qty in cart.items():
        try:
            item = Furniture.objects.get(pk=int(pk))
            subtotal = item.price * qty
            total += subtotal
            items.append({'item': item, 'qty': qty, 'subtotal': subtotal})
        except Furniture.DoesNotExist:
            pass

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            request.session['last_order'] = form.cleaned_data
            request.session['cart'] = {}
            messages.success(request, 'Замовлення оформлено! Менеджер звʼяжеться з вами для підтвердження доставки.')
            return render(request, 'store/order_success.html', {
                'order': form.cleaned_data,
                'items': items,
                'total': total,
                'cart_count': 0,
            })
    else:
        form = CheckoutForm(initial={'full_name': request.user.get_full_name() or request.user.username})

    return render(request, 'store/checkout.html', {
        'form': form,
        'cart_items': items,
        'total': total,
        'cart_count': cart_count(request),
    })


@user_passes_test(lambda user: user.is_superuser, login_url='/login/')
def add_furniture_view(request):
    if request.method == 'POST':
        form = FurnitureForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f'Товар "{item.title}" додано до каталогу.')
            return redirect('home')
    else:
        form = FurnitureForm()

    return render(request, 'store/add_furniture.html', {'form': form, 'cart_count': cart_count(request)})
