import pygame 
import os
import numpy as np
import contours

pygame.init()

keep_drawing = False

display_width = 600
display_height = 500

black = (0, 0, 0)
white = (255, 255, 255)

red = (200, 0, 0)
green = (0, 200, 0)
orange = (255,165,0)

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Digit Inference')
screen.fill(white)

def crop_img(org_img):
	cropped = pygame.Surface((display_width, 380))
	cropped.blit(org_img, (0, 0), (0, 0, 600, 380))
	return cropped

def print_output(inf):
	font = pygame.font.SysFont('', 40)
	i = 0
	for x in inf:
		text = font.render(str(x), True, (0, 0, 255))
		screen.blit(text, (21 + i, 340))
		i = i + 20

def continousline(screen, clr, start, end, radius):
    diff_x = end[0] - start[0]
    diff_y = end[1] - start[1]
    max_distance = max(abs(diff_x), abs(diff_y))
    for m in range(max_distance):
        x = int(start[0] + (float(m) / max_distance * diff_x))
        y = int(start[1] + (float(m) / max_distance * diff_y))
        pygame.draw.circle(screen, clr, (x, y), radius)

def draw_line():
	pygame.draw.line(screen, (0, 0, 0), [0, 380], [display_width, 380], 2)

running = True
while running:

	draw_line()
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			for root, _, files in os.walk('roi/'):
				for f in files:
					os.unlink(os.path.join(root, f))
			os.remove('out.png')
			running = False

		if(event.type == pygame.MOUSEBUTTONDOWN):
			keep_drawing = True
			pygame.draw.circle(screen, (0, 0, 0), event.pos, 5)

		if(event.type == pygame.MOUSEBUTTONUP):
			keep_drawing = False
			
		if(event.type == pygame.MOUSEMOTION):
			if keep_drawing:
				pygame.draw.circle(screen, (0, 0, 0), event.pos, 5)
				continousline(screen, (0, 0, 0), event.pos, last, 5)
			last = event.pos
	
	mouse = pygame.mouse.get_pos()
	
	# Ok button boundaries
	if 80+90 > mouse[0] > 80 and 400+50 > mouse[1] > 400:
		if(event.type == pygame.MOUSEBUTTONDOWN):
			pygame.draw.rect(screen, orange, (80, 400, 90, 50))  #[left, top, width, height]
			img = crop_img(screen)
			pygame.image.save(img, 'out.png')
			inf = contours.contoursFind()
			print_output(inf)
				
		if(event.type == pygame.MOUSEBUTTONUP):
			pygame.draw.rect(screen, green, (80, 400, 90, 50))

	# Clear button boundaries
	elif 420+90 > mouse[0] > 420 and 400+50 > mouse[1] > 400: 
		if(event.type == pygame.MOUSEBUTTONDOWN):
			pygame.draw.rect(screen, orange, (420, 400, 90, 50))  #[left, top, width, height]
			screen.fill(white)
		if(event.type == pygame.MOUSEBUTTONUP):
			pygame.draw.rect(screen, red, (420, 400, 90, 50))
			pygame.draw.rect(screen, green, (80, 400, 90, 50))
	else:
		pygame.draw.rect(screen, green, (80, 400, 90, 50))
		pygame.draw.rect(screen, red, (420, 400, 90, 50))

	FontSize = 33
	OkButton = pygame.font.SysFont('', FontSize)
	OkText = OkButton.render('Ok', True, (0, 0, 0))
	screen.blit(OkText, (80+(90/2)-(FontSize/2), ((400+(50/2)-(FontSize/3)))))

	#FontSize = 33
	ClearButton = pygame.font.SysFont('', FontSize)
	ClearText = ClearButton.render('Clear', True, (0, 0, 0))
	screen.blit(ClearText, (420+(90/2)-(FontSize/2)-10, ((400+(50/2)-(FontSize/3)))))

	pygame.display.update()
