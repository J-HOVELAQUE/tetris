#! /usr/bin/python3.5
# -*- coding:utf-8 -*

from tkinter import *
from figures_tetris import *
import random

class Tetris(object):

	def __init__(self,vitesse=400,):

		
		self.decor = []												# La liste des pièces déposées
		self.type_figure = [										# Liste des pièces pouvants apparaitre
				LDroite, LGauche,
				 Barre, Carre, Truc,
				 S, SInverse
				 ]	
		self.vitesse = vitesse										# Vitesse du jeu
		self.point = 0
		self.level = 0

		self.perdu = False

		self.pause = False

		schema_ligne = [0]*12
		self.schema = []
		creer_une_ligne = 20
		while creer_une_ligne != 0:
			self.schema.append([0]*12)
			creer_une_ligne -= 1

		self.root = Tk()
		self.root.title("TETRIS")
		self.aire = Canvas(self.root, height=400, width=240)		# Aire de jeu
		self.aire.create_text(2,120,text="""
				Flèche Bas, Droite et Haut
				pour déplacer la pièce
				Flèche Haut pour la faire pivoter
				Espace = Pause
				Escape pour quitter


				Presse Enter pour commencer""")

		self.affichage_score = Label(self.root, text="Niveau : {}	Score : {}".format(self.level, self.point))
		
		self.affichage_score.pack(side='top')
		self.aire.pack()

		self.root.bind("<Escape>", self.quitter)
		self.root.bind("<space>", self.onpause)
		self.root.bind("<Return>", self.commencer)

#		self.generer_figure()										# Tirer une figure

#		self.jouer()												# Lancer le jeu

		self.root.mainloop()

		#############################

		#	La méthode 'routine'	#

		#############################

	def commencer(self, *event):

		"""Pour lancer le jeu"""

		self.root.unbind("<Return>")
		self.aire.delete(ALL)
		self.generer_figure()
		self.jouer()
		

	def jouer(self):

		"""Un 'tour' de jeu"""

		### Faire descendre la figure d'un pas

		if self.pause is False and self.perdu is False:
			try:
				self.figure.descendre()
			except CollisionError:
				self.deposer_piece()

		### Recomencer

		if self.perdu is False and self.pause is False:
			self.aire.after(self.vitesse,self.jouer)

		#########################################################

		#		Méthodes pour gérer les cas particuliers		#

		#########################################################

	

	def generer_figure(self):

		"""Tirer une nouvelle figure de la liste et valider des lignes"""

		### Instanciation de la nouvelle figure

		self.figure = random.choice(self.type_figure)(self.aire,110,0)

		### Affectation des commandes claviers à la figure

		self.root.bind("<Up>",self.tourner)
		self.root.bind("<Left>", self.gauche)
		self.root.bind("<Right>", self.droite)
		self.root.bind("<Down>", self.descendre)

	def deposer_piece(self):

		"""Lorsque la pièce touche le fond ou un obstacle"""

		
		### Mettre le schéma à jour

		for carre in self.figure.root:

			if self.perdu is True:
				break

			coor_carre = (int(self.aire.coords(carre)[0]/20),int(self.aire.coords(carre)[1]/20))
			self.schema[coor_carre[1]][coor_carre[0]] = 1


		### La pièce rejoint la liste des obstacles

			self.aire.itemconfigure(carre, tag="obstacle")
			self.decor.append(carre)

		### REgarder si le joueur a perdu

			if self.aire.coords(carre)[1] <= 0:
				self.perdu = True
				self.perdre()

		### Regarder si une ligne est complète

		bonus = 0
		
		for i, ligne in enumerate(self.schema):

			if 0 not in ligne:
				self.enlever_ligne(i)

		###	Tirer une npuvelle figure	

		self.generer_figure()

	def enlever_ligne(self, numero_ligne):

		"""Enlève une ligne lorsqu'elle est complète et fait descendre toutes les autres"""

		### Fait disparaitre la ligne en question

		for carre in self.aire.find_withtag("obstacle"):
			if self.aire.coords(carre)[1] == numero_ligne*20 and self.aire.coords(carre)[3] == numero_ligne*20+20:
				self.aire.itemconfigure(carre, tag='detruit')
				
				self.aire.delete(carre)

		### Fait descendre les lignes supérieures

		for carre in self.aire.find_withtag("obstacle"):
			if self.aire.coords(carre)[1] < numero_ligne*20:
				self.aire.move(carre, 0, 20)

		### Met le schéma à jour

		del self.schema[numero_ligne]
		self.schema.insert(0, [0]*12)

		### Augmenter le score

		self.point +=1
		self.affichage_score.configure(text="Niveau : {}	Score : {}".format(self.level, self.point))
		if self.point % 10 == 0:
			self.level_up()

	def level_up(self):

		"""Passer au niveau suivant"""

		self.level +=1
		self.vitesse -= 25
		self.affichage_score.configure(text="Niveau : {}	Score : {}".format(self.level, self.point))

		
	def perdre(self):


		self.onpause()

		self.aire.delete(ALL)
		self.aire.create_text(100,100, text='PERDU')
		self.aire.after(2000,self.root.destroy)


			#############################################

			#		Méthodes liées aux commandes		#

			#############################################


	def gauche(self, *event):

		"""Déplace la piece à gauche"""

		if self.perdu is False and self.pause is False:
			self.figure.deplacer_gauche()

	def droite(self, *event):

		"""Déplacer le pièce à droite"""

		if self.perdu is False and self.pause is False:
			self.figure.deplacer_droite()

	def descendre(self, *event):

		"""Pour accélérer la déscente de la pièce"""

		if self.perdu is False and self.pause is False:
			try:
				self.figure.descendre()
			except CollisionError:
				self.deposer_piece()

	def tourner(self, *event):

		"""Pour faire tourner la pièce"""

		if self.perdu is False and self.pause is False:
			self.figure.nouvelle_rotation()

	def onpause(self, *event):

		"""Pour mettre le jeu en pause"""

		if self.pause is False:
			self.pause = True

		else:
			self.pause = False
			self.jouer()

	def quitter(self, *event):

		self.root.destroy()




if __name__ == "__main__":
	jeu = Tetris()
