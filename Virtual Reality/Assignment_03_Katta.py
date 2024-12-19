'''
1 - Pause the banner animation 
2 - Play the banner animation 
3 - Pause all animations 
4 - Play all animations 
5 - Change the walk animation speed 
6 - Female avatar fights
9 - Male avatar movement
i - zoom in
o - zoom out
'''
# Import necessary Vizard modules
import viz
import vizact
import vizinfo
import vizinput
# Set display properties
viz.setMultiSample(8)
viz.fov(30)
viz.go()
vizinfo.InfoPanel()
viz.move([6,0,-5])
# Define functions for zooming in and out
def zoom_in():
    viz.MainView.move([0, 0, -1])
def zoom_out():
    viz.MainView.move([0, 0, 1])
# Define key actions for zooming
vizact.onkeydown('i', zoom_in)
vizact.onkeydown('o', zoom_out)
# Add static objects to the scene
viz.addChild('ground.osgb')
hospital = viz.addChild('Hospital.osgb')
hospital.setPosition([-46, 0, -42.5])  
hospital.setScale([0.1, 0.15, 0.1])
foodtruck = viz.addChild('foodtruck.osgb')
foodtruck.setPosition([-15, 0, 16])  
foodtruck.setScale([1, 1, 1])
temple = viz.addChild('Greek_Temple.osgb')
temple.setPosition([-0.5,0,20.5])
temple.setScale([0.09,0.09,0.09])
viz.clearcolor(viz.SKYBLUE)
# Add animations and define key actions for animation control
animations = viz.add('piazza_animations.osgb')
vizact.onkeydown('1',animations.setAnimationState,viz.PAUSE,node='banner_sequence')
vizact.onkeydown('2',animations.setAnimationState,viz.PLAY,node='banner_sequence')
vizact.onkeydown('3',animations.setAnimationState,viz.PAUSE)
vizact.onkeydown('4',animations.setAnimationState,viz.PLAY)
vizact.onkeydown('5',animations.setAnimationSpeed,3.0,node='walk')
# Add avatar and set its parent for animation synchronization
avatar = viz.addAvatar('vcc_male2.cfg')
avatar.setParent(animations,node='walk')
avatar.state(2)
# Add additional avatars for demonstration purposes
avatar1 = viz.addAvatar('vcc_male.cfg', pos=(-5,0,10), euler=(0,0,0) )
vizact.onkeydown('9', avatar1.state, 9)
avatar2 = viz.addAvatar('vcc_female.cfg', pos=(-5.5,0,10), euler=(1,0,0) )
vizact.onkeydown('6', avatar2.state, 6)
# Prompt for participant number and add pigeon avatar
subject = vizinput.input('What is the participant number?')
pigeon = viz.addAvatar('pigeon.cfg',pos=[-5, 1.85, 10],euler=[100,0,0])
pigeon.state(1)
# Add text objects for critical question and answer options
critical_question = viz.addText('Do you see a pigeon?',viz.SCREEN)
yes = viz.addText('Yes!',viz.SCREEN)
no = viz.addText('No!',viz.SCREEN)
critical_question.alignment(viz.ALIGN_CENTER_TOP)
critical_question.setPosition(.5,.9)
yes.alignment(viz.ALIGN_LEFT_TOP)
yes.setPosition(.25,.75)
no.alignment(viz.ALIGN_LEFT_TOP)
no.setPosition(.75,.75)
# Add buttons for yes and no answers
yes_button = viz.addButton()
yes_button.setPosition(.22,.71)
no_button = viz.addButton()
no_button.setPosition(.72,.71)
# Initialize variables for timing and data storage
start_time = viz.tick()
question_data = open('pigeon_data.txt','a')
text_objects = [critical_question, yes, no, yes_button, no_button]
# Define callback function for button press events
def onbutton(obj,state):
    global text_objects
    elapsed_time = viz.tick() - start_time
    if obj == yes_button:
        data = 'Subject ' + str(subject) + ' saw a pigeon.\t'
    if obj == no_button:
        data = 'Subject ' + str(subject) + ' did not see a pigeon.\t'
    data = data + 'Elapsed time was: ' + str(round(elapsed_time,2)) + ' seconds\n'
    question_data.write(data)
    question_data.flush()
    for text_object in text_objects:
        text_object.remove()
    display_quiz()
# Register button press callback
viz.callback(viz.BUTTON_EVENT,onbutton)
# Define quiz questions and correct answers
questions = [
    "Which key is used to pause the banner animation",
    "Which key is used to play all animations",
    "Which key is used to change the walk animation speed", 
    "Which key is used to move female avatar",
    "Which key is used to zoom out",
]
correct_answers = [1, 4, 5, 6, 'o']
# Define function to display and process the quiz
def display_quiz():
    for question in questions:
        answers = vizinput.input(question + "\nYour answer: ")
    if answers in correct_answers:
      viz.addText("Correct! You answered correctly.")
    else:
      viz.addText("Incorrect! Check the tutorial for answers")
# Add a virtual instructor avatar for assistance
instructor = viz.addAvatar('vcc_female.cfg', pos=[5, 0, 0], euler=[0, 0, 0])