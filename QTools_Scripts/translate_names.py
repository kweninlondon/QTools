import bpy
import googletrans  # Install this library if needed: pip install googletrans==4.0.0-rc1

translator = googletrans.Translator()

for obj in bpy.data.objects:
    try:
        translated_name = translator.translate(obj.name, src='ko', dest='en').text
        obj.name = translated_name  # Rename object
    except Exception as e:
        print(f"Error translating {obj.name}: {e}")

print("Translation complete!")
