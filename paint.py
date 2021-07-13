import pygame, copy
from math import sqrt
from tkinter import *
from tkinter import filedialog
pygame.init()

sc = pygame.display.set_mode((600, 400))

class Tools:
	def __init__(self):
		self.gradient = pygame.transform.scale(pygame.image.load("gradient.png"), (100, 100))
		self.vis_gradient = False
	def distance(self, p1, p2):
		return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

	def save_img(self, img):
		try:
			root = Tk()
			root.overrideredirect(1)
			root.withdraw()
			path = filedialog.asksaveasfilename()
			root.destroy()
			pygame.image.save(img, path)
		except:
			pass

	def show_gradient(self, pos):
		if self.vis_gradient:
			sc.blit(self.gradient, pos)
			m_pos = pygame.mouse.get_pos()
			canvas[interface.current_frame].current_color = sc.get_at(m_pos)

class Paint_surface:
	def __init__(self, res, pixel):
		self.canvas = pygame.Surface((res[0]*pixel, res[1]*pixel))
		self.res = res
		self.canvas_pos = (50, 50)
		self.collide = self.canvas.get_rect(topleft=self.canvas_pos)
		self.canvas_color = (255, 255, 255)
		self.pixel_size = pixel
		self.paint_pos = [[[False, (0, 0, 0)] for x in range(res[0])] for y in range(res[1])]
		self.saved_frames = [self.paint_pos]
		self.current_color = (0, 0, 0)
		self.erase = False

	def correct_len_cheakpoint(self):
		if len(self.saved_frames) >= 10:
			del self.saved_frames[0]

	def draw(self):
		self.canvas.fill(self.canvas_color)
		for y, y_v in enumerate(self.paint_pos):
			for x, x_v in enumerate(y_v):
				if x_v[0]:
					pygame.draw.rect(self.canvas, x_v[1], [x*self.pixel_size, y*self.pixel_size, self.pixel_size, self.pixel_size])
		sc.blit(self.canvas, self.canvas_pos)

	def resize_canvas(self, size):
		self.canvas = pygame.transform.scale(self.canvas, size)
		self.collide = self.canvas.get_rect(topleft=self.canvas_pos)

	def draw_on_canvas(self):
		pos = pygame.mouse.get_pos()
		y_p, x_p = (pos[0]-self.canvas_pos[0]) // self.pixel_size, (pos[1]-self.canvas_pos[1]) // self.pixel_size
		self.paint_pos[x_p][y_p][0] = not self.erase
		self.paint_pos[x_p][y_p][1] = self.current_color


class Interface:
	def __init__(self):
		self.font = pygame.font.Font(None, 35)
		pygame.mouse.set_visible(False)
		self.canvas_button_radius = 10
		self.resize_button_pos = None
		self.current_frame = 0
		self.k_s = False #key's status
		self.s_s = False #save status

	def show_cursor(self):
		if not pygame.mouse.get_visible():
			c = canvas[self.current_frame]
			pos = pygame.mouse.get_pos()
			pygame.draw.circle(sc, c.current_color, pos, c.pixel_size//2)
			pygame.draw.circle(sc, (255, 255, 255), pos, c.pixel_size//2, 1)

	def draw_number_cur_frame(self):
		text = self.font.render(str(self.current_frame), 0, (255, 255, 255))
		sc.blit(text, (10, 10))

	def draw_current_color(self):
		c = canvas[self.current_frame]
		pygame.draw.rect(sc, (255, 255, 255), (49, 1, 49, 49), 1)
		pygame.draw.rect(sc, c.current_color, (51, 3, 45, 45))

	def draw_resize_button(self):
		c = canvas[self.current_frame]
		pos = c.canvas.get_width() + c.canvas_pos[0], c.canvas.get_height() + c.canvas_pos[1]
		self.resize_button_pos = pos
		pygame.draw.circle(sc, (255, 0, 0), pos, self.canvas_button_radius)

	def draw_move_canvas_button(self):
		c = canvas[self.current_frame]
		pygame.draw.circle(sc, (0, 255, 0), c.canvas_pos, self.canvas_button_radius)

	def draw_tools_menu(self):
		pygame.draw.rect(sc, (0, 0, 0), [0, 0, 600, 50])

	def do_resize(self):
		c = canvas[self.current_frame]
		offset = self.resize_button_pos[0] - c.canvas_pos[0], self.resize_button_pos[1] - c.canvas_pos[1]
		if offset[1] <= len(c.paint_pos) * c.pixel_size and offset[0] <= len(c.paint_pos[0]) * c.pixel_size:
			c.resize_canvas(offset)

	def do_move(self):
		c = canvas[self.current_frame]
		c.canvas_pos = pygame.mouse.get_pos()
		c.collide.topleft = c.canvas_pos

	def cheak_events(self):
		mouse_pos = pygame.mouse.get_pos()
		mouse_status = pygame.mouse.get_pressed()
		c = canvas[self.current_frame]
		keys = pygame.key.get_pressed()
		if mouse_status[0]:
			if not self.s_s:
				c.saved_frames.append(copy.deepcopy(c.paint_pos))
				self.s_s = True
			if tool.distance(self.resize_button_pos, mouse_pos) < self.canvas_button_radius:
				self.resize_button_pos = mouse_pos
				self.do_resize()
			elif tool.distance(c.canvas_pos, mouse_pos) < self.canvas_button_radius:
				self.do_move()
			else:
				if c.collide.collidepoint(mouse_pos):
					c.draw_on_canvas()
		else:
			self.s_s = False
		if keys[pygame.K_SPACE]:
			c.resize_canvas((c.res[0]*c.pixel_size, c.res[1]*c.pixel_size))
			c.canvas_pos = (50, 50)
		if keys[pygame.K_s]:
			tool.save_img(c.canvas)
		if keys[pygame.K_LEFT] and self.current_frame - 1 >= 0:
			if not self.k_s:
				self.current_frame -= 1
				self.k_s = True
		elif keys[pygame.K_e]:
			if not self.k_s:
				c.erase = not c.erase
				self.k_s = True
		elif keys[pygame.K_n]:
			if not self.k_s:
				canvas.append(Paint_surface((25, 25), 10))
				self.k_s = True
				self.current_frame = len(canvas) - 1 
		elif keys[pygame.K_TAB]:
			if not self.k_s:
				self.k_s = True
				tool.vis_gradient = not tool.vis_gradient
		elif keys[pygame.K_RIGHT] and self.current_frame + 1 <= len(canvas)-1:
			if not self.k_s:
				self.current_frame += 1
				self.k_s = True
		elif keys[pygame.K_z] and keys[pygame.K_LCTRL]:
			if not self.k_s:
				if len(c.saved_frames) > 0:
					c.paint_pos = c.saved_frames[-1]
					c.saved_frames.pop()

				self.k_s = True
		else:
			self.k_s = False

tool = Tools()
canvas = [Paint_surface((25, 25), 10)]
interface = Interface()

while True:
	[exit() for i in pygame.event.get() if i.type == pygame.QUIT]
	sc.fill((0, 0, 20))
	canvas[interface.current_frame].draw()
	canvas[interface.current_frame].correct_len_cheakpoint()
	interface.draw_tools_menu()
	interface.draw_resize_button()
	interface.draw_move_canvas_button()
	interface.draw_number_cur_frame()
	interface.draw_current_color()
	tool.show_gradient((50, 50))
	interface.show_cursor()
	interface.cheak_events()
	pygame.display.update()