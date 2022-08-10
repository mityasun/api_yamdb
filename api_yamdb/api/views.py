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