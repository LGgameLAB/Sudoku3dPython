import pygame
import sys, os, math
from settings import *
from pygame import Rect, Vector2, Vector3

class Cube(pygame.sprite.Sprite):
	def __init__(self, game):
		self.groups = game.renderer.spritelayers[0], game.sprites
		super().__init__(self.groups)
		self.game = game
		self.orientation = Vector3(0, 0, 0)
		self.points = [(1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1)]
		self.faces = [(0,1,2,3), (4,5,6,7), (0,1,5,4), (2,3,7,6), (1,2,6,5), (0,3,7,4)]
		self.scale = 20*FOV
		self.speed = 2
		self.zoom = 10 # This is essentially the camera's z position

	def update(self):

		o = self.orientation
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			o.y += self.game.dt()*self.speed
		if keys[pygame.K_s]:
			o.y -= self.game.dt()*self.speed
		if keys[pygame.K_d]:
			o.x += self.game.dt()*self.speed
		if keys[pygame.K_a]:
			o.x -= self.game.dt()*self.speed

	def render(self, surf, camera=False):
		if camera:
			pass
		else: 
			for f in self.faces:
				pygame.draw.polygon(surf, GREEN, [self.project(self.transform(self.points[p])) for p in f], 1)


	def transform(self, point):
		p = Vector3(point)
		o = self.orientation
		return p.rotate_x(o.x).rotate_y(o.y).rotate_z(o.z)

	def project(self, v):
		return ( self.scale*((v.x)/(self.zoom+v.z)) + self.game.win.get_width()/2, self.scale*((v.y)/(self.zoom+v.z)) + self.game.win.get_height()/2)


class Render:
	def __init__(self, game):
		self.game = game
		self.spritelayers = [pygame.sprite.Group() for x in range(3)]
		# self.overlayer = pygame.sprite.Group()

	def render(self, win):
		for s in self.spritelayers:
			for o in s:
				o.render(win)

class Game:
	def __init__(self):
		pygame.init()

		self.res = pygame.display.list_modes()
		self.win = pygame.display.set_mode(self.res[3])
		self.clock = pygame.time.Clock()
		self.renderer = Render(self)
		self.sprites = pygame.sprite.Group()
		self.fonts = [
			pygame.font.SysFont(pygame.font.get_fonts()[1], 30, False, False)
		]

		self.cube = Cube(self)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()
					break
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.quit()
				if event.type == pygame.MOUSEWHEEL:
					if event.y:
						self.cube.zoom = max(2, self.cube.zoom + event.y)

			self.win.fill(BLACK)
			self.update()
			self.renderer.render(self.win)
			self.draw_fps()
			# print(pygame.event.get_grab())
			pygame.display.update()
			self.clock.tick(60)

	def update(self):
		self.sprites.update()

	def draw_fps(self):
		self.win.blit(self.fonts[0].render(str(self.clock.get_fps()), False, WHITE), (self.win.get_width()-100, 0))

	def dt(self):
		return self.clock.get_rawtime()/self.clock.get_time()

	def quit(self):
		pygame.quit()
		sys.exit()

while __name__ == "__main__":
	p = Game();
	p.run()