import list
import board
import project as p
# import json

class Card(object):

	def __init__(self, name, project=None):
		self.name = name
		self.card_type = ""
		self.description = ""
		self.estimate = 0
		self.estimate_type = ""
		self.tags = []
		self.watchers = []
		self.assignee = ""
		self.list = ""
		self.board = ""
		self.project = project
		self.status = ""
		self.relationships = {'blocks':[],'is blocked by':[],'relates to':[], \
		'is child of':[], 'is parent of':[], 'is caused by':[], 'causes':[]}

		if project != None:
			self.project.cards.append(self)
			self.id = self.project.prefix + "-" + str((len(self.project.cards)))

		else:
			self.id = None


	def addRelationship(self, status, to_card):
		if status == "blocks":
			if to_card.name == self.name:
				raise ReferenceError('Cannot block itself')

			elif self in to_card.relationships['blocks']:
				raise ReferenceError('Creates circular dependency: a card cannot block itself')

			else:
				self.relationships['blocks'].append(to_card)
				to_card.relationships['is blocked by'].append(self)

		if status == "relates to":
			if to_card.name == self.name:
				raise ReferenceError('Cannot relate to itself')
			else:
				self.relationships['relates to'].append(to_card)
				to_card.relationships['relates to'].append(self)

		if status == "is parent of":
			if to_card.name == self.name:
				raise ReferenceError('Cannot be parent of itself')

			self.relationships['is parent of'].append(to_card)
			to_card.relationships['is child of'].append(self)

		if status == "is child of":
			if to_card.name == self.name:
				raise ReferenceError('Cannot be child of itself')
			self.relationships['is child of'].append(to_card)
			to_card.relationships['is parent of'].append(self)

		if status == "is caused by":
			if to_card.name == self.name:
				raise ReferenceError('Cannot be caused by itself')
			self.relationships['is caused by'].append(to_card)
			to_card.relationships['causes'].append(self)

		if status =="causes":
			if to_card.name == self.name:
				raise ReferenceError('Cannot cause itself')
			self.relationships['causes'].append(to_card)
			to_card.relationships['is caused by'].append(self)

		return None

	def getDocument(self):
		document = {
		"name": self.name,
		"id": self.id,
		"estimate": self.estimate,
		"estimate_type": self.estimate_type,
		"card_type": self.card_type,
		"description": self.description,
		"estimate": self.estimate,
		"tags": self.tags,
		"watchers": self.watchers,
		"assignee": self.assignee,
		"list": self.list.name,
		"board": self.board.name,
		"project": self.project.name,
		"status": self.status,
		"relationships": self.relationships
		}

		return document
