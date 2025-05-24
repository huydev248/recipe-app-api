from rest_framework import serializers

from core.models import (
    Recipe,
    Tag
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, required=False)

    def _get_or_create_tags(self, tags, recipe):
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag
            )
            recipe.tag.add(tag_obj)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tag']
        read_only_fields = ['id']

    def create(self, validated_data):
        tag = validated_data.pop('tag', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tag, recipe)

        return recipe

    def update(self, instance, validated_data):
        tag = validated_data.pop('tag', None)
        if tag is not None:
            instance.tag.clear()
            self._get_or_create_tags(tag, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
