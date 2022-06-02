from django.views.generic.base import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from . models import LikeSystem

# Create your views here.


class LikeSystemView(LoginRequiredMixin, View):
    model = None
    action_type = None
    def post(self, request, pk):
        data = dict()
        content_object = self.model.objects.get(pk=pk)

        try:
            likedislike = LikeSystem.objects.get(
                content_type=ContentType.objects.get_for_model(
                    content_object
                ),
                object_id=content_object.slug,
                user=request.user,
            )

            if likedislike.action != self.action_type:
                likedislike.action = self.action_type
                likedislike.save(update_fields=["action"])

            else:
                likedislike.delete()
        except LikeSystem.DoesNotExist:
            content_object.likesystem.create(
                action=self.action_type, user=request.user
            )


        data["likes"] = content_object.likesystem.likes().count()
        data["dislikes"] = content_object.likesystem.dislikes().count()

        return JsonResponse(data)
