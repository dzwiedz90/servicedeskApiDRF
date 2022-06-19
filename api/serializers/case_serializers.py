from rest_framework import serializers

from ..models import Case


class GetCasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'content', 'date_created', 'severity', 'is_closed', 'user', 'admin_assigned']


class CreateCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['content', 'date_created', 'severity', 'is_closed', 'user', 'admin_assigned']

        def save(self, instance, validated_data):
            instance.content = validated_data.get('content', instance.content)
            instance.date_created = validated_data.get('date_created', instance.date_created)
            instance.severity = validated_data.get('severity', instance.severity)
            instance.is_closed = validated_data.get('is_closed', instance.is_closed)
            instance.user = validated_data.get('user', instance.user)
            instance.admin_assigned = validated_data.get('admin_assigned', instance.admin_assigned)
            instance.save()
            return instance


class UpdateCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['content', 'severity']

        def update(self, instance, validated_data):
            instance.content = validated_data.get('content', instance.content)
            instance.severity = validated_data.get('severity', instance.severity)
            instance.save()
            return instance
