from rest_framework import serializers
from projects.models import Project, Tags, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'
        

class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    Tags = TagsSerializer(many=True)
    Reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
    def get_Reviews(self, obj):
        Reviews = obj.review_set.all()
        serializer = ReviewSerializer(Reviews, many=True)
        return serializer.data

