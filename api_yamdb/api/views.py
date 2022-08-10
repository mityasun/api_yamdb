from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from .serializers import (RegistrationSerializer, TokenSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация в проекте YaMDb.',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email='info@yamdb.ru',
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework import mixins, permissions, viewsets, status
from api.serializers import CategorySerializer, GenreSerializer, TitleSerializer
from reviews.models import Category, Genre, Title
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView



class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Вьюсет для модели Category"""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(detail=True, methods=['delete'])
    def delete(self, request, slug):
        title = self.get_object(slug)
        title.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(#mixins.CreateModelMixin, mixins.ListModelMixin,
                   viewsets.ModelViewSet):
    """Вьюсет для модели Genre"""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()



    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, slug):
        genre = Genre.objects.get(slug=slug)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#from rest_framework.decorators import api_view
#@api_view(['DELETE'])  # Применили декоратор и указали разрешённые методы
#def hello(request,slug):
    # По задумке, в ответ на POST-запрос нужно вернуть JSON с теми данными,
    # которые получены в запросе.
    # Для этого в объект Response() передаём словарь request.data.
    #if request.method == 'DELETE':
       # genre = Genre.objects.get(slug=slug)
      #  genre.delete()
       # return Response(status=status.HTTP_204_NO_CONTENT)

#гет и и пост ок, делит нет

    #@action(detail=True, methods=['delete'])
    #def delete(self, request, *args, **kwargs):
    #    return self.destroy(request, *args, **kwargs)
#class GenreDestroy(APIView):
    #def delete(self, request, slug):
       # genre = Genre.objects.get(slug=slug)
       # genre.delete()
       # return Response(status=status.HTTP_204_NO_CONTENT)


    #@action(detail=True, methods=['delete'])
    #def delete(self, obj):
        #slug = self.kwargs.get('slug')
        #genre = Genre.objects.get(slug=slug)
        #genre.delete()


    #def delete(self, request, slug):
      #  post = Genre.objects.get(slug=slug)
        #post.delete()
       # return Response(status=status.HTTP_204_NO_CONTENT)

class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title"""

    serializer_class = TitleSerializer
    queryset = Title.objects.all()

    def delete(self, request, slug):
        title = self.get_object(slug)
        title.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)