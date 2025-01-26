from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, resolve_url
from django.template.response import HttpResponse, TemplateResponse
from django.views.decorators.http import require_http_methods, require_safe

from .forms import TodoForm
from .models import TodoItem
from .response import HttpResponseSeeOther


@require_safe
def todo_list(request):
    if search := request.GET.get("q", ""):
        todo_qs = TodoItem.objects.contains_text(search)
    else:
        todo_qs = TodoItem.objects.all()

    context = {
        "todo_count": todo_qs.count(),
        "todo_list": todo_qs,
        "search_term": search,
    }
    return TemplateResponse(request, "todo/list.html", context)


@require_http_methods(["GET", "HEAD", "DELETE"])
def todo_detail(request, todo_id: int):
    todo = get_object_or_404(TodoItem, id=todo_id)
    if request.method == "DELETE":
        todo.delete()
        messages.add_message(request, messages.INFO, "Deleted todo item")
        return HttpResponseSeeOther(resolve_url("todo:list"))
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
    todo.title = request.GET.get("id_title")
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
    todo = TodoItem.objects.create()
    todo.title = request.GET.get("id_title")
    try:
        todo.full_clean()
        return HttpResponse()
    except ValidationError as error:
        title_errors = error.message_dict.get("title", [])
        if not title_errors:
            return HttpResponse()
        return HttpResponse(",".join(title_errors))
