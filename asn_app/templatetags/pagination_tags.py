from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_compact_page_range(context):
    page_obj = context.get('page_obj')
    if not page_obj or not page_obj.paginator:
        return []
    total_pages = page_obj.paginator.num_pages
    current = page_obj.number
    pages = []

    if total_pages <= 7:
        for num in page_obj.paginator.page_range:
            pages.append({'num': num, 'ellipsis': False})
        return pages

    pages.append({'num': 1, 'ellipsis': False})

    if current > 3:
        pages.append({'num': None, 'ellipsis': True})

    left = max(2, current - 1)
    right = min(total_pages - 1, current + 1)

    for num in range(left, right + 1):
        pages.append({'num': num, 'ellipsis': False})

    if current < total_pages - 2:
        pages.append({'num': None, 'ellipsis': True})

    pages.append({'num': total_pages, 'ellipsis': False})

    return pages
