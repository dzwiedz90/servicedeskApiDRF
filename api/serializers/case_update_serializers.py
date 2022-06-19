from rest_framework import serializers

from ..models import CaseUpdate


class GetCaseUpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseUpdate
        fields = ['id', 'comment', 'date_created', 'user', 'case']


class CreateCaseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseUpdate
        fields = ['comment', 'date_created', 'user', 'case']

        def save(self, instance, validated_data):
            instance.comment = validated_data.get('comment', instance.comment)
            instance.date_created = validated_data.get('date_created', instance.date_created)
            instance.user = validated_data.get('user', instance.user)
            instance.case = validated_data.get('case', instance.case)
            instance.save()
            return instance


class UpdateCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseUpdate
        fields = ['comment', 'user', 'case']

        def update(self, instance, validated_data):
            instance.comment = validated_data.get('comment', instance.comment)
            instance.user = validated_data.get('user', instance.user)
            instance.case = validated_data.get('case', instance.case)
            instance.save()
            return instance
