from django.shortcuts import render
import requests
from openai import OpenAI
from PIL import Image
from io import BytesIO
from django.conf import settings
import os
from .secret import api_key

client = OpenAI(api_key=api_key)
topic="array and pointers"

def index(request):
    # created_script = script(topic)
    # img = image_creation(created_script)
    return render(request, 'index.html',{'script':'created_script','img':'img'})

def generate(request):
    topic=request.POST.get('topic')
    if topic:
        created_script = script(topic)
        print(created_script)
        img = image_creation(created_script)
        return render(request, 'conten.html',{'script':created_script,'img':img})
    else:
        return render(request, 'conten.html',{'script':'','img':''})


def script(topic):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Meme prompt creator with no text"},
        {"role": "user", "content": topic}
    ]
    )
    print("\nscript called !!\n")
    return completion.choices[0].message.content

def image_creation(script):

    # Generate image
    response = client.images.generate(
        model="dall-e-2",
        prompt=script,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # Get the URL of the generated image
    image_url = response.data[0].url

    # Download the image
    image_response = requests.get(image_url)

    # Check if the request was successful
    if image_response.status_code == 200:
        # Open the image using PIL
        image = Image.open(BytesIO(image_response.content))

        # Save the image
        static_directory = settings.STATICFILES_DIRS[0]
        image_path = os.path.join(static_directory, "generated_image.jpg")
        image.save(image_path)
        print(image_path)
        # image.save("generated_image.jpg")
        # Display the image
        print("created image!!")
    else:
        print("Failed to download the image.") 
    return image_path