from rest_framework import serializers
from .models import Music,Artist,CSVFile
from datetime import datetime, date

# Create your views here.


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'
        read_only_fields = ['id']


    def validate(self, data):
            title = data.get('title')
            album_name = data.get('album_name')
            if title and album_name and title == album_name:
                raise serializers.ValidationError("Title and album name should not be the same.")

            return data

                    
        

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id','name','dob','gender','address','first_release_year','no_of_albums_released','created_at','updated_at']    
        read_only_fields = ['id']
        

    def validate_no_of_albums_released(self, value):
        current_year = date.today().year
        print(current_year)
        if value <= 0:
            raise serializers.ValidationError('No of albums released must be a greater than 0.')
        return value        

    def validate_dob(self, value):
        print('value',value)
        if value and value.date() >= date.today():
            raise serializers.ValidationError('Date of birth must be in the past.')
        return value

class MusicArtistSerializer(serializers.ModelSerializer):
    musics = MusicSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'

import datetime
import csv
class CSVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVFile
        fields = ['id', 'file']
        read_only_fields = ['id']

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError('Only CSV files are allowed.')

        try:
            decoded_file = value.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines())

            header = next(csv_data)  # Skip the header row

            for row in csv_data:
                if len(row) != len(header):
                    raise serializers.ValidationError(
                        'Please arrange your values in the following format for import:\n'
                        'name,gender,address,first_release_year,no_of_albums_released\n'
                        'John Doe,Male,123 Main Street,2022-02-04,1'
                    )

                # Perform additional validation for each row
                # Example: Validate first_release_year field
                first_release_year = row[3].strip()
                try:
                    datetime.datetime.strptime(first_release_year, '%Y-%m-%d')
                except ValueError:
                    raise serializers.ValidationError(
                        'Please arrange your values in the following format for import:\n'
                        'name,gender,address,first_release_year,no_of_albums_released\n'
                        'John Doe,Male,123 Main Street,2022-02-04,1'
                    )
        except UnicodeDecodeError:
            raise serializers.ValidationError('Unable to decode the CSV file. Please ensure the file is in UTF-8 encoding.')

        return value