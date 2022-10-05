# class TestSerializer(serializers.ModelSerializer):
#
#     def validate_question(self, value):
#         raise serializers.ValidationError("Blog post is not about Django")
#
#     class Meta:
#         model = Questions
#         fields = '__all__'
#
#
# @action(methods=['get'], detail=False, url_path='test1')
# def vs_test(self, request):
#     serializer = TestSerializer(data=request.data)
#     serializer.is_valid()
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
