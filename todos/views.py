"""
Views for the todos app.
"""

from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Todo
from .serializers import TodoSerializer, TodoUpdateSerializer


class IsOwner(permissions.BasePermission):
    """Object-level permission: only the todo owner can access it."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


@extend_schema(tags=["Todos"])
@extend_schema_view(
    get=extend_schema(
        operation_id="todo_list",
        summary="List todos",
        description="Returns a list of todos for the currently authenticated user.",
        parameters=[
            OpenApiParameter("is_completed", bool, description="Filter by completion status"),
            OpenApiParameter("priority", str, description="Filter by priority (low/medium/high)"),
            OpenApiParameter("search", str, description="Search in title and description"),
            OpenApiParameter("ordering", str, description="Order by field (e.g. created_at, due_date, priority)"),
        ],
    ),
    post=extend_schema(
        operation_id="todo_create",
        summary="Create a todo",
        request={"multipart/form-data": TodoSerializer},
    ),
)
class TodoListCreateView(APIView):
    """List all todos for the authenticated user or create a new one."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class=TodoSerializer
    
    def get_queryset(self, request):
        qs = Todo.objects.filter(owner=request.user)
        is_completed = request.query_params.get("is_completed")
        priority = request.query_params.get("priority")
        search = request.query_params.get("search")
        ordering = request.query_params.get("ordering", "-created_at")

        if is_completed is not None:
            qs = qs.filter(is_completed=is_completed.lower() in ("true", "1", "yes"))
        if priority:
            qs = qs.filter(priority=priority.lower())
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(description__icontains=search)

        allowed_orderings = {"created_at", "-created_at", "due_date", "-due_date", "priority", "-priority"}
        if ordering in allowed_orderings:
            qs = qs.order_by(ordering)

        return qs

    def get(self, request):
        qs = self.get_queryset(request)
        serializer = TodoSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = TodoSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Todos"])
@extend_schema_view(
    get=extend_schema(operation_id="todo_retrieve", summary="Retrieve a todo"),
    put=extend_schema(
        operation_id="todo_update",
        summary="Update a todo (full)",
        request={"multipart/form-data": TodoUpdateSerializer},
    ),
    patch=extend_schema(
        operation_id="todo_partial_update",
        summary="Update a todo (partial)",
        request={"multipart/form-data": TodoUpdateSerializer},
    ),
    delete=extend_schema(operation_id="todo_destroy", summary="Delete a todo"),
)
class TodoDetailView(APIView):
    """Retrieve, update, or delete a single todo (owner only)."""

    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class=TodoSerializer

    def get_object(self, pk, request):
        try:
            obj = Todo.objects.get(pk=pk, owner=request.user)
            self.check_object_permissions(request, obj)
            return obj
        except Todo.DoesNotExist:
            return None

    def get(self, request, pk):
        todo = self.get_object(pk, request)
        if todo is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        todo = self.get_object(pk, request)
        if todo is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TodoUpdateSerializer(todo, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        todo = self.get_object(pk, request)
        if todo is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TodoUpdateSerializer(todo, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo = self.get_object(pk, request)
        if todo is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
