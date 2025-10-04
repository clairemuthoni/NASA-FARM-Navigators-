import asyncio
import pygame
import random

class Crop:
    def __init__(self):
        self.no = 10
        self.ndvi = 1

crop_field = []

for h in range(24):
    crop_field.append([])
    for w in range(32):
        crop_field[h].append(Crop())
        
        
rainfall = []
for i in range(365):
    rainfall.append(random.randint(0, 800))

pygame.init()
pygame.display.set_mode((800, 600))
surface = pygame.display.get_surface();
clock = pygame.time.Clock()

colors = [(151, 76, 1), (126, 134, 74), (188, 219, 90), (147, 193, 0)]

ndvi_levels = [0, 0.33, 0.66, 1]

start_image = pygame.image.load("img/start.png")

rain_img = pygame.surface.Surface((25, 25))
rain_img.set_colorkey((0, 0, 0))

pygame.draw.rect(rain_img, (0, 178, 193), (0, 0, 2, 6))
pygame.draw.rect(rain_img, (0, 178, 193), (4, 10, 2, 6))
pygame.draw.rect(rain_img, (0, 178, 193), (3, 7, 2, 6))
pygame.draw.rect(rain_img, (0, 178, 193), (7, 20, 2, 6))
pygame.draw.rect(rain_img, (0, 178, 193), (15,15, 2, 6))
pygame.draw.rect(rain_img, (0, 178, 193), (19, 8, 2, 6))

async def main():
    is_running = True

    while is_running:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                
        surface.fill((255, 255, 255))
        
        # surface.blit(start_image, (0, 0))
        
        for h in range(24):
            for w in range(32):
                crop: Crop = crop_field[h][w]
                color = ()
                for i in range(len(ndvi_levels)):
                    if crop.ndvi <= ndvi_levels[i]:
                        color = colors[i]
                        break
                    
                pygame.draw.rect(surface, color, (w*25, h*25, 25, 25))
                
                
        for i in range(25):
            x = random.randint(0, 10)
            y = random.randint(0, 10)
            crop_field[y][x].ndvi -= 0.1
            if crop_field[y][x].ndvi < -1:
                crop_field[y][x].ndvi = -1
                
        # for h in range(24):
        #     for w in range(32):
        #         surface.blit(rain_img, (w*25, h*25))
                        
        
        pygame.display.update()
        await asyncio.sleep(0)  # You must include this statement in your main loop. Keep the argument at 0.
        
        clock.tick(5)

    pygame.quit()

asyncio.run(main())
