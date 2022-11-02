from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag()
def hourtemp(current_page,loop_num):
    offset = abs(current_page - loop_num)
    if offset < 3:  # If the absolute value of the current number of cycles and the number of currently displayed pages is less than 3,The page number is displayed
        if current_page == loop_num:
            # If the looping page is the current display page,Then add the background color
            # first loop_num Page number for transfer,the second loop_num For the,
            page_ele = '''<li class="active"><a href="?page= %s">%s<span class="sr-only">(current)</span></a></li>''' % (
            loop_num, loop_num)
        else:
            page_ele = '''<li class=""><a href="?page= %s">%s<span class="sr-only">(current)</span></a></li>''' % (
            loop_num, loop_num)
        return format_html(page_ele)  # with html Back to front end
    else:
        return ''