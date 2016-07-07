import card as c
import board as b
import list as l
import project as p
import separator as s
import organization as o
import sys
from pymongo import MongoClient


# -------------------------
# GLOBAL Variables
# -------------------------


number_of_passed_tests = 0
number_of_tests_run = 0
list_of_tests_passed = []
failures = {}

#######################################
#									  #
# 			General Methods           #
#									  #
#######################################

def runTestSuite():
	print "\nStarting tests...\n"


	# Functionality of the MongoDB Database
	canAddCardToDB()
	canEditCardData()

    # Functionality of an organization
	canCreateOrganization()

	# Functionality of a project
	canCreateProject()
	canAddBoardToProject()
	#canGetListOfBoardNames()

	# Functionality of a Board
	canCreateBoard()
	canAddBoardDescription()
	canCreateList()
	canGetListIndex()


	# Functionality of a List
	canAddCardToList()
	canAddSeparatorToList()
	canMoveItemToTopOfList()
	canMoveItemToBottomOfList()
	canDuplicateItem()
	canAssignAttributeToAllCardsInList()


	# Functionality of a Card
	canCreateCard()
	canGetDocument()
	canGetCardUniqueID()
	canAssignCardAttributes()
	canAssignCardRelationship()

	# Functionality of a Separator
	canCreateSeparator()

	return testResults() + listFailedTests()

	# NOTE: Can add "+ listPassedTests()" to print a list of passed tests

def passTest(test_name):
	global number_of_passed_tests
	global number_of_tests_run

	number_of_passed_tests += 1
	list_of_tests_passed.append(test_name)
	number_of_tests_run += 1

def failTest(test_name, fail_cause):
	global number_of_tests_run

	number_of_tests_run +=1
	failures[test_name] = fail_cause

def testResults():
	return "--------------------\n%d of %d tests passed.\n--------------------" \
	% (number_of_passed_tests, number_of_tests_run)

def listPassedTests():
	results = "\nThe following tests passed: \n"

	for passed_test in list_of_tests_passed:
		results += "- " + passed_test + "\n"

	return results

def listFailedTests():
	results = "\n"
	if number_of_passed_tests != number_of_tests_run:
		results += "\n \n The following tests failed: \n"
		i = 1

		for item in failures:
			results += str(i) + ". " + item + ": %r \n" % failures[item]
			i += 1
	else:
		results += "\n"
	return results

def createTestOrganization(*num_orgs):
	if len(num_orgs) == 0:
		ret = o.Organization("test_org")
	else:
		ret = []
		for i in range(num_projects[0]):
			temp_org = o.Organization("test_org_" + str(i))
			ret.append(temp_org)
	return ret

def createTestProject(*num_projects):
	if len(num_projects) == 0:
		ret = p.Project("test_project")
	else:
		ret = []
		for i in range(num_projects[0]):
			temp_project = p.Project("test_project_" + str(i))
			ret.append(temp_project)
	return ret

def createTestBoard():
	board = b.Board("test")
	return board

def createTestCard(*num_cards):
	test_project = p.Project("test_project")
	test_list = l.List("test_list")
	test_board = b.Board("test_board")

	if len(num_cards) == 0:


		ret = c.Card("test")
		ret.name = "OEM Install Requirements"
		ret.type = "Task"
		ret.description = "This is the ret description"
		ret.estimate = "4"
		ret.tags.append("OEM")
		ret.watchers.append("Stephen")
		ret.assignee = "Matt"
		ret.list = test_list
		ret.board = test_board
		ret.project = test_project
		ret.status = "In Progress"

	elif len(num_cards) == 1:
		ret = []
		for i in range(num_cards[0]):
			temp_card = c.Card("test_card_" + str(i))
			temp_card.type = "Task"
			temp_card.description = "This is the temp_card description"
			temp_card.estimate = "4"
			temp_card.tags.append("OEM")
			temp_card.watchers.append("Stephen")
			temp_card.assignee = "Matt"
			temp_card.list = test_list
			temp_card.board = test_board
			temp_card.project = test_project
			temp_card.status = "In Progress"
			ret.append(temp_card)
	else:
		ret = []
		for i in range(num_cards[0]):
			temp_card = c.Card("test_card_" + str(i), num_cards[1])
			temp_card.type = "Task"
			temp_card.description = "This is thetemp_card description"
			temp_card.estimate = "4"
			temp_card.tags.append("OEM")
			temp_card.watchers.append("Stephen")
			temp_card.assignee = "Matt"
			temp_card.list = test_list
			temp_card.board = test_board
			temp_card.project = test_project
			temp_card.status = "In Progress"
			ret.append(temp_card)

	return ret

def createTestList():
	list = l.List("test")
	return list

def createPopulatedList(num_cards):
	test_list = createTestList()
	cards = createTestCard(num_cards)

	for i in range(len(cards)):
			test_list.addCard(cards[i])

	return test_list

def createTestSeparator():
	separator = s.Separator("test")
	return separator

def canary():
	print "*!*!*! Canary *!*!*!"


#######################################
#									  #
#  Tests for Database Objects	      #
#									  #
#######################################

def canAddCardToDB():
	test_name = "Database: Can add a card object to the DB"

	try:
		card = createTestCard()

		client = MongoClient()
		db = client.cardCeption
		result = db.cards.insert_one(card.getDocument())
		if result.inserted_id != None:
			passTest(test_name)
		else:
			failTest(test_name, "Logic Error")
	except:
		failTest(test_name, sys.exc_info()[1])

def canEditCardData():
	test_name = "Database: Can edit card data"

	try:
		card = createTestCard()
		client = MongoClient()
		db = client.cardCeption
		result = db.cards.insert_one(card.getDocument())

		db.cardCeption.update_one(
			{"name": card.name},
			{
				"$set": {"type":"epic"},
				"$currentDate": {"lastModified": True}

			}
		)
		passTest(test_name)
	except:
		failTest(test_name, sys.exc_info()[1])



#######################################
#									  #
#  Tests for Organization Objects     #
#									  #
#######################################

def canCreateOrganization():
    test_name = "Can create organization"

    try:
        org = o.Organization("test_org")
        passTest(test_name)
    except:
        failTest(test_name, sys.exc_info()[1])

#######################################
#									  #
#    Tests for Project Objects        #
#									  #
#######################################

def canCreateProject():
	try:
		project = p.Project("Project")
		if project.name == "Project":
			passTest("Create a project")
		else:
			failTest("Create a project", "Logic error in Project Class")
	except:
		failTest("Create a project", sys.exc_info()[1])

def canAddBoardToProject():

	try:
		project = p.Project("test_project")
		project.addBoard("test_board")
		project.addBoard("test_board2")
		boardsList = project.getListOfBoardNames()

		if boardsList[0] == "test_board" and boardsList[1] == "test_board2":
			passTest("Add a Board to a Project")
		else:
			failTest("Add a board to a Project", "Reason Unknown")
	except:
			failTest("Add a Board to a Project", sys.exc_info()[1])

# TO DO

def canAddProjectStartDate():
	return None

def canAddProjectDueDate():
	return None

#######################################
#									  #
#    Tests for Board Objects          #
#									  #
#######################################


def canCreateBoard():
	test_name = "Board: Create a board"
	try:
		board = createTestBoard()
		passTest(test_name)
	except:
		failTest(test_name, sys.exc_info()[1])

def canAddList():
	test_name = "Board: Add a list to a board"
	try:
		createTestBoard("board")
		board.addList("List 1")
		passTest(test_name)
	except:
		failTest(test_name, sys.exc_info()[1])

def canAddBoardDescription():
	test_name = "Board: Can add board decription"
	try:
		board = createTestBoard()
		board.addDescription("This is the description of the board")
		if board.description == "This is the description of the board":
			passTest(test_name)
		else:
			failTest(test_name, "Reason Unknown")
	except:
		failTest(test_name, sys.exc_info()[1])

#######################################
#									  #
#    Tests for List  Objects          #
#									  #
#######################################

def canCreateList():
	test_name = "List: Create a List"

	try:
		board = createTestBoard()
		board.addList("test_list")
		passTest(test_name)
	except:
		failTest(test_name, sys.exc_info()[1])

def canGetListIndex():
	test_name = "List: Can get list index on board"

	try:
		board = createTestBoard()
		for i in range(0,3):
			board.addList(i)
		if board.getListIndex("0") == 0:
			passTest(test_name)
		else:
			failTest(test_name, sys.exc_info()[1])
	except:
		failTest(test_name, sys.exc_info()[1])

def canAddSeparatorToList():
	test_name = "List: Add Separator to List"
	try:
		list = createTestList()
		separator = createTestSeparator()
		list.addSeparator(separator)
		passTest(test_name)
	except:
		failTest(test_name, sys.exc_info()[1])

def canAddCardToList():
	test_name = "List: Add Card to List"
	try:
		list = createTestList()
		card = createTestCard()
		list.addCard(card)
		passTest(test_name)
	except:
		failTest(test_name, sys.exc_info()[1])

def canMoveItemToTopOfList():
	test_name = "List: Move item to top of list"

	try:
		list = createTestList()
		card = createTestCard(10)

		for i in range(len(card)):
			list.addCard(card[i])

		test_item_name = list.items[4].name

		list.moveItemToTop(4)

		if test_item_name == list.items[0].name:
			passTest(test_name)
		else:
			failTest(test_name, "Logic Error in MoveToTop method in List Class")

	except:
		failTest(test_name, sys.exc_info()[1])

def canMoveItemToBottomOfList():
	test_name = "List: Move item to bottom of list"

	try:
		list = createTestList()
		card = createTestCard(10)

		for i in range(len(card)):
			list.addCard(card[i])

		test_item_name = list.items[6].name

		list.moveItemToBottom(6)

		if test_item_name == list.items[len(list.items) - 1].name:
			passTest(test_name)
		else:
			failTest(test_name, "Logic error in MoveItemToBottom method in List Class")
	except:
		failTest(test_name, sys.exc_info()[1])

def canDuplicateItem():
	test_name = "List: Duplicate an item on a list"

	try:
		from_board = createTestBoard()
		to_board = createTestBoard()
		from_list = createTestList()
		to_list = createTestList()
		to_board.addList(to_list)
		cards = createTestCard(10)

		for i in range(len(cards)):
			from_list.addCard(cards[i])

		test_card_name = from_list.items[3].name
		from_list.duplicateItem(3, to_board, to_list)

		to_list_index = 0
		for i in range(len(to_board.lists)):
			if to_board.lists[i] == to_list.name:
				to_list_index = i

		b =  to_board.lists[to_list_index].items[len(to_board.lists[to_list_index].items)-1].name
		if test_card_name == b:
			passTest(test_name)
		else:
			failTest(test_name, "Logic error in duplicateCard method in List class")

	except:
		failTest(test_name, sys.exc_info()[1])

def canAssignAttributeToAllCardsInList():
	test_name = "List: Assign attribute to all cards in list"

	try:
		# Create a test list with cards and separators
		# in random places
		test_list = createPopulatedList(10)
		test_list.items.append(createTestSeparator())
		test_list.moveItem(len(test_list.items)-1,4)
		test_list.items.append(createTestSeparator())
		test_list.moveItem(len(test_list.items)-1,6)
		test_list.items.append(createTestSeparator())
		test_list.moveItem(len(test_list.items)-1,0)

		test_list.assignAttributeToAll("type", "Task")



		for i in range(len(test_list.items)):
			if type(test_list.items[i]) == c.Card and test_list.items[i].type != "Task":
				failTest(test_name, "Logic error in assignAttributeToAll method in class List")
				break
		passTest(test_name)
	except:
		failTest(test_name, sys.exc_info()[1])

# ---------- To Do ----------

def canMoveItemToPositionOnSameList():
	test_name = "Move a card to a position in the same list"

	try:
		list = createTestList()
		card = createTestCard(10)

		for i in range(len(card)):
			list.addCard(card[i])


		# Move card at index 4 to index 6
		# NOTE: includes zeroth position
		test_card_1_name = list.items[3].name
		list.moveItem(3, 6)

		print "---"
		print test_card_1_name
		print list.items[0].name
		print "---"


		test_card_2_name = list.items[4].name
		list.moveItem(4,3)

		print test_card_2_name
		print list.items[3].name
		print "---"



		if list.items[0].name == test_card_1_name and list.items[6].name == test_card_2_name:
			 passTest(test_name)
		else:
			failTest(test_name, "Logic Error in moveItem method in List class")

	except:
		failTest(test_name, sys.exc_info()[1])



	return None

def canMoveCardToPositionOnDifferentList():
	return None

def canMoveCardToTopOfSection():
	return None

def canMoveCardToBottomOfSection():
	return None

#######################################
#									  #
#    Tests for Card Objects           #
#									  #
#######################################

def canCreateCard():
	test_name = "Card: Create a card"
	try:
		card = createTestCard()
		passTest(test_name)
	except:
		failTest(test_name, sys.exc_info()[1])

def canAssignCardAttributes():
	test_name = "Card: Assign attributes to a card"
	try:
		test_list = createTestList()
		test_board = createTestBoard()
		test_project = createTestProject()
		cards = createTestCard(10)

		card = createTestCard()
		card.name = "Name"
		card.type = "Task"
		card.description = "This is the card description"
		card.estimate = "4"
		card.tags.append("OEM")
		card.watchers.append("Stephen")
		card.assignee = "Matt"
		card.list = test_list
		card.board = test_board
		card.project = test_project
		card.status = "In Progress"
		passTest(test_name)

	except:
		failTest(test_name, sys.exc_info()[1])

def canAssignCardRelationship():
	test_name = "Assign Card Relationships"
	cards = createTestCard(10)

	try:
		# Testing for relationship creation
		cards[1].addRelationship("blocks",cards[2])
		cards[1].addRelationship("relates to",cards[3])
		cards[1].addRelationship('is parent of',cards[5])
		cards[1].addRelationship('is child of', cards[7])
		cards[1].addRelationship('is caused by', cards[4])
		cards[1].addRelationship('causes',cards[8])

		# Testing that circular dependencies are caught
		try:
			cards[2].addRelationship("blocks",cards[1])
			# TO DO:
			# - Add more circular dependencies
		except ReferenceError:
			passTest(test_name)


	except:
		failTest(test_name, sys.exc_info()[1])

def canGetDocument():
	test_name = "Card: Get MongoDB Document for a Card"
	card = createTestCard()

	try:
		card.getDocument()
		passTest(test_name)
	except:
		failTest(test_name, sys.exc_info()[1])


########## TO DO ##########

def canGetCardUniqueID():
	test_name = "Each card has a unique ID"

	try:
		projects = createTestProject(2)
		for i in range(len(projects)):
			cards = createTestCard(3, projects[i])

		passTest(test_name)

	except:
		failTest(test_name, sys.exc_info()[1])


def canEditCardDependencies():
	return None

def canGetCardAge():
	return None




#######################################
#									  #
#    Tests for Separator Objects      #
#									  #
#######################################


def canCreateSeparator():
	try:
		separator = createTestSeparator()
		passTest("Create a Separator")
	except:
		failTest("Create a Separator", sys.exc_info()[1])

### START ###

print runTestSuite()
