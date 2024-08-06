from django.core.management.base import BaseCommand
from map3d.models import SuperCam
import csv
import os

class Command(BaseCommand):
    help = 'Your batch processing description here'

    def handle(self, *args, **options):
        # csvファイルが格納されているディレクトリのパス
        csv_directory = "/code/map3d/management/commands/csv"
        
        # csvファイルのリストを取得
        csv_files = [file for file in os.listdir(csv_directory) if file.endswith(".csv")]
        
        # 各csvファイルからデータを抽出
        for csv_file in csv_files:
            csv_path = os.path.join(csv_directory, csv_file)
        
            file_name = ''
            obs_id = ''
            wavelength = ''
            reflectance = ''
        
            with open(csv_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                
                print(f"Data from {csv_file}:")
                for row in csv_reader:
                    if csv_reader.line_num == 1: 
                        file_name = row[0]
                        obs_id = row[1]
                        latitude = row[2]
                        longitude = row[3]
        
                    if csv_reader.line_num == 2:
                        wavelength = ','.join(map(str, row))
        
                    if csv_reader.line_num == 3:
                        reflectance = ','.join(map(str, row))
            
            SuperCam.objects.create(file_name=file_name, obs_id=obs_id, longitude=longitude, latitude=latitude, csv_wavelength=wavelength, csv_reflectance=reflectance)

        self.stdout.write(self.style.SUCCESS('Batch processing completed successfully'))