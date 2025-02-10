from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, resolve_url
from django.template.response import HttpResponse, TemplateResponse
from django.views.decorators.http import require_http_methods, require_safe

from .forms import TodoForm
from .models import TodoItem
from .response import HttpResponseSeeOther


@require_safe
def todo_list(request):
    page_number = request.GET.get("page", 1)
    if search := request.GET.get("q", ""):
        todo_qs = TodoItem.objects.contains_text(search)
    else:
        todo_qs = TodoItem.objects.all()
    paginator = Paginator(todo_qs, 10)

    if request.headers.get("HX-Trigger") == "search":
        template = "todo/todo_rows.html"
    else:
        template = "todo/list.html"

    context = {
        "todo_list": paginator.get_page(page_number),
        "search_term": search,
    }
    return TemplateResponse(request, template, context)


@require_safe
def todo_count(request):
    todo_count = TodoItem.objects.slow_count()
    return HttpResponse(f"There are { todo_count } items.")


@require_http_methods(["GET", "HEAD", "DELETE"])
def todo_detail(request, todo_id: int):
    todo = get_object_or_404(TodoItem, id=todo_id)
    if request.method == "DELETE":
        todo.delete()
        if request.headers.get("HX-Trigger") == "delete-btn":
            messages.add_message(request, messages.INFO, "Deleted todo item")
            return HttpResponseSeeOther(resolve_url("todo:list"))
        return HttpResponse("")
    # this is GET or HEAD
    return TemplateResponse(request, "todo/detail.html", {"todo": todo})


@require_http_methods(["GET", "HEAD", "POST"])
def todo_create(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            new_todo = form.save()
            messages.add_message(
                request, messages.INFO, f"Created new todo item: {new_todo.id}, {new_todo.title}"
            )
            return redirect("todo:list")
        # if form is not valid, leave it with errors for redisplay
    else:
        form = TodoForm()
    return TemplateResponse(request, "todo/new.html", {"form": form})


@require_http_methods(["GET", "HEAD", "POST"])
def todo_edit(request, todo_id: int):
    todo = get_object_or_404(TodoItem, id=todo_id)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            new_todo = form.save()
            messages.add_message(
                request, messages.INFO, f"Updated todo item: {new_todo.id}, {new_todo.title}"
            )
            return redirect("todo:list")
        # if form is not valid, leave it with errors for redisplay
    else:
        form = TodoForm(instance=todo)
    return TemplateResponse(
        request, "todo/edit.html", {"form": form, 'todo_id': todo.id}
    )


@require_safe
def title_check(request, todo_id: int):
    todo = get_object_or_404(TodoItem, id=todo_id)
    todo.title = request.GET.get("title")
    try:
        todo.full_clean()
        return HttpResponse()
    except ValidationError as error:
        title_errors = error.message_dict.get("title", [])
        if not title_errors:
            return HttpResponse()
        return HttpResponse(",".join(title_errors))


@require_safe
def title_check_new(request):
    todo = TodoItem()
    todo.title = request.GET.get("title")
    try:
        todo.full_clean()
        return HttpResponse()
    except ValidationError as error:
        title_errors = error.message_dict.get("title", [])
        if not title_errors:
            return HttpResponse()
        return HttpResponse(",".join(title_errors))
