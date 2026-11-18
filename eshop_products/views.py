from django.http import Http404
from django.views.generic.list import ListView

from product_category.models import Product_category
from .models import product , Product_gallery
from django.shortcuts import get_object_or_404, render
from django.db.models import Q , Count
from eshop_order.forms import User_neworder_Form
class ProductlistView(ListView):
    template_name = 'products/products.html'
    paginate_by = 5

    def get_queryset(self):
        return product.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']
        context['page_range'] = self._page_range(page_obj, on_each_side=1)
        context['counts'] = dict(
            Product_category.objects.annotate(
                c=Count('product', filter=Q(product__active=True), distinct=True)
            ).values_list('name', 'c')
        )
        return context

    @staticmethod
    def _page_range(page_obj, on_each_side=1):
        number = page_obj.number
        num_pages = page_obj.paginator.num_pages
        ELLIPSIS = page_obj.paginator.ELLIPSIS

        if num_pages <= 1:
            return [1] if num_pages == 1 else []

        start = max(1, number - on_each_side)
        end   = min(num_pages, number + on_each_side)

        pages = list(range(start, end + 1))

        if num_pages > end:
            if num_pages - end > 1:
                pages.append(ELLIPSIS)
            pages.append(num_pages)

        return pages



class ProductlistView_category(ProductlistView):
    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        if not category_name:
            raise Http404('صفحه مورد نظر یافت نشد')

        categories = Product_category.objects.filter(name__iexact=category_name)
        if not categories.exists():
            raise Http404('صفحه مورد نظر یافت نشد')

        return product.objects.filter(
            active=True, cetegories__in=categories
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.kwargs.get('category_name', '')
        return context



def product_detail(request, product_id, title):
    Product = get_object_or_404(product, id=product_id, active=True)
    new_order_from = User_neworder_Form(request.POST or None,initial=({'product_id': product_id}))


    gallery = Product_gallery.objects.filter(
        product_id=product_id,
        image__isnull=False,
    ).exclude(image='')

    LIMIT = 6
    related = list(
        product.objects.filter(
            active=True,
            cetegories__in=Product.cetegories.all()
        ).exclude(pk=Product.pk).distinct()[:LIMIT]
    )

    if len(related) < LIMIT:
        existing_ids = [p.pk for p in related] + [Product.pk]
        fill = product.objects.filter(active=True).exclude(
            pk__in=existing_ids
        ).order_by('-time')[:LIMIT - len(related)]
        related += list(fill)
    Product.visits += 1
    Product.save()

    context = {
        'product': Product,
        'related_products': related,
        'gallery': gallery,
        'new_order_from' : new_order_from,
    }
    return render(request, 'products/product_detail.html', context)
class SearchProduct(ProductlistView):
    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        qs = product.objects.filter(active=True)

        if query:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(tag__title__icontains=query)
            ).distinct()

        return qs