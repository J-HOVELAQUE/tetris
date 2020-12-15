#! /usr/bin/python3.5
# -*- coding:utf-8 -*

from tkinter import *
from random import randrange


class Figure(object):

	"""La classe générique pour les figures"""

	def __init__(self,aire,centrex,centrey):


		self.aire = aire									#  Rattachement à l'aire de jeu
		self.centre = (centrex,centrey)						#  Centre de la figure



	def nouvelle_rotation(self, *event):

		valide = True		# Pour vérifier que le mouvement est possible
		new_fig = []		# Coordonnées de tous les carrés de la nouvelle figure

		for i, carre in enumerate(self.root):

		## Determiner les coordonnées des centres des carres par rapport au centre

			newcoords = [
					self.aire.coords(carre)[0] - self.centre[0],
					self.aire.coords(carre)[1] - self.centre[1],
					self.aire.coords(carre)[2] - self.centre[0],
					self.aire.coords(carre)[3] - self.centre[1]
			]
			
		## Appliquer la rotation

			newcoords_tourne = [
					-(newcoords[1]),
					newcoords[0],
					-(newcoords[3]),
					newcoords[2]
			]

		## Nouvelles coordonnées sur le plan:

			real_newcoords = [
					newcoords_tourne[0] + self.centre[0],
					newcoords_tourne[1] + self.centre[1],
					newcoords_tourne[2] + self.centre[0],
					newcoords_tourne[3] + self.centre[1]
					]

			new_fig.append(real_newcoords)

		## Verifier que le mouvement est possible

			# Contre un obstacle
			for touch in self.aire.find_withtag("obstacle"):

				if touch in self.aire.find_overlapping\
				(real_newcoords[0]-5,real_newcoords[1]-5,\
					real_newcoords[2]+5,real_newcoords[3]+5):

					valide = False
					break
	
			# Contre un bord
			if real_newcoords[2] < 0 or real_newcoords[0] > 250:
				valide = False
			elif real_newcoords[3] > 400:
				valide = False
				
		## Appliquer le mouvement

		if valide is True:
			for i, carre in enumerate(self.root):
				self.aire.coords(carre,new_fig[i][0],new_fig[i][1],new_fig[i][2],new_fig[i][3])

			
	def deplacer_gauche(self, *event):

		valide = True
		new_fig = []


		for carre in self.root:
			newcoords = [
			self.aire.coords(carre)[0]-20,
			self.aire.coords(carre)[1],
			self.aire.coords(carre)[2]-20,
			self.aire.coords(carre)[3]
			]

			new_fig.append(newcoords)

		## Verifier que le mouvement est possible

			# Contre un obstacle
			for touch in self.aire.find_withtag("obstacle"):

				if touch in self.aire.find_overlapping\
					(newcoords[0]+5,newcoords[1]+5,\
					newcoords[2]-5,newcoords[3]-5):

					valide = False
					break
	
			# Contre un bord
			if newcoords[0] < 0 or newcoords[2] > 250:
				valide = False
			elif newcoords[3] > 400:
				valide = False

		## Appliquer le mouvement si possible

		if valide is True:

			for i, carre in enumerate(self.root):
				self.aire.coords(carre,new_fig[i][0],new_fig[i][1],new_fig[i][2],new_fig[i][3])

			self.centre = (self.centre[0]-20, self.centre[1])  #  Déplacer le centre de la pièce


	def deplacer_droite(self, *event):

		valide = True
		new_fig = []

		for carre in self.root:
			newcoords = [
			self.aire.coords(carre)[0]+20,
			self.aire.coords(carre)[1],
			self.aire.coords(carre)[2]+20,
			self.aire.coords(carre)[3]
			]

			new_fig.append(newcoords)


			## Verifier que le mouvement est possible

			# Contre un obstacle
			for touch in self.aire.find_withtag("obstacle"):

				if touch in self.aire.find_overlapping\
					(newcoords[0]+5,newcoords[1]+5,\
					newcoords[2]-5,newcoords[3]-5):

					valide = False
					break
	
			# Contre un bord
			if newcoords[0] < 0 or newcoords[2] > 250:
				valide = False
			elif newcoords[3] > 400:
				valide = False

		## Appliquer le mouvement si possible

		if valide is True:

			for i, carre in enumerate(self.root):
				self.aire.coords(carre,new_fig[i][0],new_fig[i][1],new_fig[i][2],new_fig[i][3])

			self.centre = (self.centre[0]+20, self.centre[1])  #  Déplacer le centre de la pièce


	def descendre(self, *event):

		valide = True
		new_fig = []

		for carre in self.root:

			if len(self.aire.coords(carre)) == 0:
				valide = False
				break

			newcoords = [
			self.aire.coords(carre)[0],
			self.aire.coords(carre)[1]+10,
			self.aire.coords(carre)[2],
			self.aire.coords(carre)[3]+10
			]

			new_fig.append(newcoords)


			## Verifier que le mouvement est possible

			# Contre un obstacle
			for touch in self.aire.find_withtag("obstacle"):

				if touch in self.aire.find_overlapping\
					(newcoords[0]+5,newcoords[1]+5,\
					newcoords[2]-5,newcoords[3]-5):

					valide = False
					break
	
			# Contre un bord
			
			if newcoords[3] > 400:
				valide = False

		## Appliquer le mouvement si possible

		if valide is True:

			for i, carre in enumerate(self.root):
				self.aire.coords(carre,new_fig[i][0],new_fig[i][1],new_fig[i][2],new_fig[i][3])

			self.centre = (self.centre[0], self.centre[1]+10)  #  Déplacer le centre de la pièce

		elif valide is False:

			raise CollisionError("Fond touché")



		#########################

		#	Types de figures	#

		#########################


class LGauche(Figure):

	def __init__(self,aire,centrex,centrey):

		Figure.__init__(self,aire,centrex,centrey)

		centres_des_carres=[
		(self.centre[0],self.centre[1]-20),
		(self.centre[0],self.centre[1]),
		(self.centre[0],self.centre[1]+20),
		(self.centre[0]-20,self.centre[1]+20)
		]
			
		self.root = []
		
		for carre in centres_des_carres:
			self.root.append(self.aire.create_rectangle(carre[0]-10,carre[1]-10,carre[0]+10,carre[1]+10,\
			 fill='green', tags="corp"))


class LDroite(Figure):

	def __init__(self,aire,centrex,centrey):

		Figure.__init__(self,aire,centrex,centrey)

		centres_des_carres=[
			(self.centre[0],self.centre[1]-20),
			(self.centre[0],self.centre[1]),
			(self.centre[0],self.centre[1]+20),
			(self.centre[0]+20,self.centre[1]+20)
			]
			
		self.root = []
		
		for carre in centres_des_carres:
			self.root.append(self.aire.create_rectangle(carre[0]-10,carre[1]-10,carre[0]+10,carre[1]+10,\
			 fill='purple', tags="corp"))

class Barre(Figure):

	def __init__(self,aire,centrex,centrey):

		Figure.__init__(self,aire,centrex,centrey)

		centres_des_carres=[
		(self.centre[0],self.centre[1]-20),
		(self.centre[0],self.centre[1]),
		(self.centre[0],self.centre[1]+20),
		(self.centre[0],self.centre[1]+40)
		]

		self.root = []
		
		for carre in centres_des_carres:
			self.root.append(self.aire.create_rectangle(carre[0]-10,carre[1]-10,carre[0]+10,carre[1]+10,\
			 fill='red', tags="corp"))


class Carre(Figure):

	def __init__(self,aire,centrex,centrey):

		Figure.__init__(self,aire,centrex,centrey)
		self.centre = (centrex+10,centrey)

		centres_des_carres=[
			(self.centre[0]-10,self.centre[1]-10),
			(self.centre[0]+10,self.centre[1]-10),
			(self.centre[0]-10,self.centre[1]+10),
			(self.centre[0]+10,self.centre[1]+10)
			]
			
		self.root = []
		
		for carre in centres_des_carres:
			self.root.append(self.aire.create_rectangle(carre[0]-10,carre[1]-10,carre[0]+10,carre[1]+10,\
			 fill='blue', tags="corp"))

class Truc(Figure):

	def __init__(self,aire,centrex,centrey):

		Figure.__init__(self,aire,centrex,centrey)

		centres_des_carres=[
		(self.centre[0]-20,self.centre[1]),
		(self.centre[0],self.centre[1]),
		(self.centre[0]+20,self.centre[1]),
		(self.centre[0],self.centre[1]-20)
		]	

		self.root = []

		for carre in centres_des_carres:
			self.root.append(self.aire.create_rectangle(carre[0]-10,carre[1]-10,carre[0]+10,carre[1]+10,\
			 fill='yellow', tags="corp"))

class S(Figure):

	def __init__(self,aire,centrex,centrey):

		Figure.__init__(self,aire,centrex,centrey)
		self.centre = (centrex+10,centrey)

		centres_des_carres=[
		(self.centre[0]-30,self.centre[1]+10),
		(self.centre[0]-10,self.centre[1]+10),
		(self.centre[0]-10,self.centre[1]-10),
		(self.centre[0]+10,self.centre[1]-10)
		]	

		self.root = []

		for carre in centres_des_carres:
			self.root.append(self.aire.create_rectangle(carre[0]-10,carre[1]-10,carre[0]+10,carre[1]+10,\
			 fill='cyan', tags="corp"))

class SInverse(Figure):

	def __init__(self,aire,centrex,centrey):

		Figure.__init__(self,aire,centrex,centrey)
		self.centre = (centrex+10,centrey)

		centres_des_carres=[
		(self.centre[0]-10,self.centre[1]-10),
		(self.centre[0]+10,self.centre[1]-10),
		(self.centre[0]+10,self.centre[1]+10),
		(self.centre[0]+30,self.centre[1]+10)
		]	

		self.root = []

		for carre in centres_des_carres:
			self.root.append(self.aire.create_rectangle(carre[0]-10,carre[1]-10,carre[0]+10,carre[1]+10,\
			 fill='brown', tags="corp"))


class CollisionError(Exception):

	"""Exception levée lors d'une collision avec le bas de la pièce"""

	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message



if __name__ == "__main__":
	test = Tk()
	surface = Canvas(test, height=200, width=200)
	surface.pack()
	figure = S(surface, 90,100)
#	surface.create_rectangle(110,100,130,120,fill='black', tag='obstacle')
#	surface.create_rectangle(20,100,40,120,fill='black', tag='obstacle')
	test.bind("<Return>", figure.nouvelle_rotation)
	test.bind("<Left>", figure.deplacer_gauche)
	test.bind("<Right>", figure.deplacer_droite)
	test.mainloop()

