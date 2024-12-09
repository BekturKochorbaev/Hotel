from rest_framework import serializers
from .models import *


class ChangePasswordSerializer(serializers.Serializer):
    model = UserProfile
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['hotel_image']

class HotelSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = '__all__'

    def get_photos(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(photo.hotel_image.url) for photo in obj.hotel_images.all()] if request else []

    def get_rating(self, obj):
        return obj.reviews.aggregate(avg_stars=models.Avg('stars'))['avg_stars'] or 0

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['room_image']

class RoomSerializer(serializers.ModelSerializer):
    hotell_room = serializers.SlugRelatedField(
        slug_field='name_hotel',
        queryset=Hotel.objects.all()
    )
    photos = RoomImageSerializer(source='room_images', many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all(),
        required=False,
        allow_null=True
    )
    user_name = serializers.SlugRelatedField(
        slug_field='username',
        queryset=UserProfile.objects.all()
    )
    hotel = serializers.SlugRelatedField(
        slug_field='name_hotel',
        queryset=Hotel.objects.all()
    )

    class Meta:
        model = Review
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    hotel_book = serializers.SlugRelatedField(
        slug_field='name_hotel',
        queryset=Hotel.objects.all()
    )
    room_book = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all()
    )
    user_book = serializers.SlugRelatedField(
        slug_field='username',
        queryset=UserProfile.objects.all()
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'

    def get_total_price(self, obj):
        return (obj.check_out_date - obj.check_in_date).days * obj.room_book.room_price

    def validate(self, data):
        room = data.get('room_book')
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')

        conflicting_bookings = Booking.objects.filter(
            room_book=room,
            check_in_date__lte=check_out_date,
            check_out_date__gte=check_in_date,
            status_book__in=['Бронь', 'подверждено']
        )
        if conflicting_bookings.exists():
            raise serializers.ValidationError('Комната уже забронирована на выбранные даты.')
        return data


