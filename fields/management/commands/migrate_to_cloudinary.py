import os
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from fields.models import Field
from cloudinary.uploader import upload

class Command(BaseCommand):
    help = 'Migrate existing field images to Cloudinary'

    def handle(self, *args, **kwargs):
        fields = Field.objects.exclude(image='')
        
        if not fields.exists():
            self.stdout.write(self.style.WARNING('No fields with images found.'))
            return
        
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for field in fields:
            if field.image and field.image.url and not field.image.url.startswith('http://res.cloudinary.com'):
                try:
                    self.stdout.write(f'Processing {field.name}...')
                    
                    # Check if the image file exists
                    image_path = field.image.path if hasattr(field.image, 'path') else None
                    
                    if image_path and os.path.exists(image_path):
                        # Upload to Cloudinary
                        result = upload(
                            image_path, 
                            folder='field_images/',
                            public_id=f'field_{field.id}'
                        )
                        
                        # Update the field with Cloudinary URL
                        field.image = result['secure_url']
                        field.save()
                        
                        self.stdout.write(self.style.SUCCESS(f'✓ Migrated {field.name}'))
                        success_count += 1
                    else:
                        self.stdout.write(self.style.WARNING(f'⚠ Skipped {field.name} - image file not found locally'))
                        skip_count += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ Failed to migrate {field.name}: {e}'))
                    error_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\nMigration complete! Success: {success_count}, Skipped: {skip_count}, Errors: {error_count}'))