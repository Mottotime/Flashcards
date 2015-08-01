#Flashcards.py
#	This program is an electronic version of flashcard review for vocabulary building or 
#whatever else. It works from a text file named 'flashcard_content.txt' which needs to 
#formatted like a list, each card on its own line:
#		['item 1', 'answer 1]
#		['item 2', 'answer 2]
#		['item 3', 'answer 3]
#	If that file doesn't already exist, the program creates it and allows new cards to be 
#filled into the file in proper formatting. It's easiest not to enter cards manually.
#You can enter a 1 when you know the card well enough, and a different file named 
#'flashcard_scores.txt' will save accumulated correct answers. This way, when review order
#[4] is selected the easier cards will be shown last and the more difficult cards or the
#ones that haven't been reviewed yet will be shown first.

from random import shuffle

#display a card
def show_card(side1,side2):
	print "\n",side1
	ans=raw_input("    Enter 'q' to quit and 1 if you know the card: ")
	print "        ",side2
	if(ans=='delete'):
		return -2
	elif(ans=='q'):
		return -1
	elif(ans=='1'):
		return 1
	else:
		return 0

#randomize the order of elements in an array		
def array_shuffle(A):
	x=[[i] for i in range(len(A))]
	shuffle(x)
	B=[0]*len(A)
	for i in range(len(A)):
		B[i]=A[x[i][0]]
	return B

#check if a file exists or can be opened in a given mode	
def check_file_exists(filepath, mode):
	try:
		f=open(filepath, mode)
		f.close()
	except IOError as err:
		return False
	return True	

#load the word-definition pairs into a list
if(check_file_exists("flashcard_content.txt","r")):
	cards=[]
	with open("flashcard_content.txt","r") as ifile:
		for line in ifile:
			temp=eval(line)
			if(len(temp[0])>0 and len(temp[1])>0):
				cards.append(temp)
	print "\n", len(cards), "cards",
else:
	with open("flashcard_content.txt","w") as ofile:
		ofile.write('[]')
	cards=[]
	print "\nThe file 'flashcard_content.txt' has been created for new flashcards\n"

#prepare scoring array
#check if the scoring file exists, create one if it doesn't
if(not check_file_exists('flashcard_scores.txt','r')):
	ifile=open('flashcard_scores.txt','w')
	ifile.write('[]')
	ifile.close
#load scores from the file, expanding the scoring array if needed
with open("flashcard_scores.txt","r") as ifile:
	scores=eval(ifile.read())
if(len(scores)==0):
	scores=[0]*len(cards)
elif(len(scores)<len(cards)):
	diff=len(cards)-len(scores)
	scores=scores+[0]*diff
	print ",",diff,"were added since the last review",

#review loop
more='y'
while(more=='y'):
	if(len(cards)==0):
		print "There are no flashcards, you must add some."
		choice=5
	else:
		print "\n\nChoose a review order or add cards."
		print "\n[1] Forward\n [2] Backward\n  [3] Randomized\n   [4] Past performance"
		print "    [5] Add cards"
		choice=int(raw_input("\nSelection: "))
	while(choice<1 or choice>5):
		choice=int(raw_input("Select an option between 1 and 5 inclusive: "))
	if(choice==5):
		print "\nEnter 'q' to stop adding cards",
		while True:
			side1=raw_input('\n\nEnter the front side of the new card: ')
			if(side1=='q'):
				break
			side2=raw_input('\nEnter the back side of the new card: ')
			if(side2=='q'):
				break
			cards.append([side1,side2])
	else:
		print "\nDo you want to do the cards front-side up or back-side up?"
		print "\n[1] Front-side up\n [2] Back-side up"
		choice2=int(raw_input("\nSelection: "))
		while(choice2<1 or choice2>2):
			choice=int(raw_input("Select an option between 1 and 2 inclusive: "))
		if choice2==2:
			for i in range(len(cards)):
				temp=cards[i][0]
				cards[i][0]=cards[i][1]
				cards[i][1]=temp
		print "\nEnter '1' when you know the card, 'delete' to delete it, and 'q' to quit."
		#run through the words in index order
		if(choice==1):
			for i in range(len(cards)):
				ans=show_card(cards[i][0],cards[i][1])
				if(ans==1):
					scores[i]+=1
				elif(ans==-1):
					break
				elif(ans==-2):
					cards.pop(i)
					scores.pop(i)
		#reverse index order
		elif(choice==2):
			for i in range(len(cards)-1,-1,-1):
				ans=show_card(cards[i][0],cards[i][1])
				if(ans==1):
					scores[i]+=1
				elif(ans==-1):
					break
				elif(ans==-2):
					cards.pop(i)
					scores.pop(i)
		#randomized order
		elif(choice==3):
			idx=range(len(cards))
			idx=array_shuffle(idx)
			for i in idx:
				ans=show_card(cards[i][0],cards[i][1])
				if(ans==1):
					scores[i]+=1
				elif(ans==-1):
					break
				elif(ans==-2):
					cards.pop(i)
					scores.pop(i)
		#ordered so that more difficult words come first and the first group of words with
		#the same past performance scores are randomized 
		elif(choice==4):
			#bubble sort the indices according to their corresponding scores
			idx=range(0,len(scores))
			found=0;
			while(not found):
				found=1
				for i in range(len(cards)-1):
					if(scores[idx[i]]>scores[idx[i+1]]):
						temp=idx[i];
						idx[i]=idx[i+1]
						idx[i+1]=temp
						found=0
			#randomize the order of all words with the lowest score
			low=scores[idx[0]]
			count=1
			idx2=[idx[0]]
			while(scores[idx[count]]==low and count<len(idx)-1):
				idx2.append(idx[count])
				count+=1
			if(count==len(idx)-1 and scores[idx[count]]==low):
				idx2.append(idx[count])
			idx2=array_shuffle(idx2)
			for i in range(len(idx2)):
				idx[i]=idx2[i]
			#review through the words in the newly created order
			for i in range(len(cards)):
				ans=show_card(cards[idx[i]][0],cards[idx[i]][1])
				if(ans==1):
					scores[idx[i]]+=1
				elif(ans==-1):
					break
				elif(ans==-2):
					cards.pop(i)
					scores.pop(i)
		if choice2==2:
			for i in range(len(cards)):
				temp=cards[i][0]
				cards[i][0]=cards[i][1]
				cards[i][1]=temp
	
	#write performance scores and potentially altered word list back into the text file, 
	#even if the review is quit before all of the words were displayed			
	with open("flashcard_scores.txt","w") as ofile:
		ofile.write(str(scores))
	with open("flashcard_content.txt","w") as ofile:
		for line in cards:
			ofile.write("%s\n" % line)
			
	if(quit==-1):
		break
		
	more=raw_input("\nEnter y to review again: ")