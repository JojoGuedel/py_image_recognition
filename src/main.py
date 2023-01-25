import io
import urllib.request
import pygame

import CPVAPI

# from PIL import Image, ImageDraw, ImageFont

IMAGE = 'https://www.vmcdn.ca/f/files/victoriatimescolonist/json/2022/03/web1_vka-viewstreet-13264.jpg'

# def download(image_url):
#     r = requests.get(image_url, stream = True)

#     if r.status_code == 200:
#         # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
#         r.raw.decode_content = True
        
#         # Open a local file with wb ( write binary ) permission.
#         with open('./data/image.jpg','wb') as f:
#             shutil.copyfileobj(r.raw, f)
        
#         print('Image sucessfully downloaded')
#     else:
#         print('Image Couldn\'t be retreived')

running = True

def load_key():
    with open('./data/key', 'r') as file:
        return file.read()

def load_image_file(image_url):
    raw_data = urllib.request.urlopen(image_url).read()
    return io.BytesIO(raw_data)

def poll_events():
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

def main():
    response = CPVAPI.try_get(IMAGE, load_key())
    if response is None:
        print("")
        return
    
    image = pygame.image.load(load_image_file(IMAGE))
    
    pygame.init()
    canvas = pygame.display.set_mode(image.get_size(), pygame.DOUBLEBUF)
    
    s = pygame.Surface(image.get_size())
    s.set_alpha(100)
    
    font = pygame.font.SysFont(None, 24)
    
    objects = response.objects
    for object in objects:
        print(f'{object.object} with {object.confidence} confidence.')

    while running:
        poll_events()

        mouse_pos = pygame.mouse.get_pos()
        
        canvas.fill((255, 255, 255))
        canvas.blit(image, (0, 0))

        for object in objects:
            rect = pygame.Rect(object.rectangle.pos, object.rectangle.size)
            if rect.collidepoint(mouse_pos):
                text = font.render(f'Object: {object.object}', False, (255, 0, 0))
                canvas.blit(text, (10, 10))

            pygame.draw.rect(s, (255, 0 , 0), rect)
        canvas.blit(s, (0, 0))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()