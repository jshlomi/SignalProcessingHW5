import sys
import numpy as np
import random

import string
letters = string.ascii_lowercase+' ,.'


transition_dictLog = np.load('dict.npy')
transition_dictLog = transition_dictLog.item()


def garble(sentence, garble_prob_threshold):

    new_sentence = ''

    for letter in sentence:
        if letter.lower() in letters:
            garble_prob = random.uniform(0, 1)
            if garble_prob < garble_prob_threshold:
                rand_letter = letters[random.randint(0,len(letters)-1)]
                new_sentence+=rand_letter
            else:
                new_sentence+=letter.lower()


    return new_sentence

def logProbMultiply(logp,logq):
    if logp == '-infinity' or logq == '-infinity':
        return '-infinity'
    else:
        return logp+logq

def logProbAddition(logp, logq):
    #ln(e^p+e^q) = p + ln(e^(q-p) + 1)
    if logp == '-infinity' and logq == '-infinity':
        return '-infinity'
    if logp == '-infinity':
        return logq
    if logq == '-infinity':
        return logp

    if logp > logq:
        return logp + np.log(1.0+ np.exp(logq-logp))
    else:
        return logq + np.log(1.0+ np.exp(logp-logq))

def emissionProb(y,x,garbleProb,nStates):
    if x==y:
        return (1-garbleProb)+garbleProb*1.0/float(nStates)
    else:
        return garbleProb*1.0/float(nStates)



def pOutputSequence(output_sentence,states,markovModel,garbleProb):

    seqLength = len(output_sentence)

    numberOfStates = len(states)

    ProbMatrix = np.zeros((numberOfStates,seqLength))

    for t in range(0,seqLength):
        yT = output_sentence[t]

        for i, state in enumerate(states):

            xT = state

            emission = np.log( emissionProb(yT,xT,garbleProb,numberOfStates) )

            if t==0: #filling the first column, we dont need to sum of previous states

                ProbMatrix[i][t] = emission

            else:

                sumOfProbs = '-infinity' # we start with prob=0

                for j in range(len(states)):
                    ## the calculation we need is
                    ## (prob sum over previous states where the last state was state_j)
                    ## * (transitionProbability j to state_i )

                    #the sum over previous states (log(p))
                    previousSum = ProbMatrix[j][t-1]

                    xTminus1 = states[j]

                    transitionProb = markovModel[xTminus1][xT]

                    #remember previousSum and transitionProb are log probablities,
                    # and we need to multiply them (so add the logs),
                    # and then add the probabilities

                    sumOfProbs = logProbAddition( sumOfProbs ,  logProbMultiply( previousSum , transitionProb ) )

                #this is multiplication of probabilites, so simple addition is enough
                ProbMatrix[i][t] = logProbMultiply( emission , sumOfProbs )


    FinalProb = '-infinity'
    for j in range(len(states)):

        FinalProb =  logProbAddition( FinalProb, ProbMatrix[j][seqLength-1] )

    return FinalProb



import unicodedata
import codecs

f = codecs.open('TaleOfTwoCities.txt', encoding='utf-8')
testSetlines = f.readlines()
f.close()

testSetlines = [unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').rstrip() for x in testSetlines]
testSetlines = " ".join(testSetlines)
testSetlines = "".join([x.lower() if x.lower() in letters else ' ' for x in testSetlines  ])
testSetlines = ' '.join( testSetlines.split()) #get rid of extra spaces


startingPointInTestSet = 720000
lengthOfSequences = 1000
testGarbleProb = 0.5
nTests = 40

if(len(testSetlines) < startingPointInTestSet+nTests*lengthOfSequences ):
    print ' test set too short, exit '
    exit()


testSetSplit = []
testSetSplitGarbeled = []
testSetGarbPofH1 = []
bkgSetPofH1 = []


import datetime
starttime = datetime.datetime.now()

print 'starting generating tests '+str(starttime)


percentShown = 0
for i in range( nTests ):

    percent = int ( (float(i)/nTests)*100.0 )

    if percent % 5 == 0 and percent > percentShown:
        percentShown = percent
        print ' done ', percent, ' %'

    testSetSplit.append(testSetlines[startingPointInTestSet+i*lengthOfSequences : startingPointInTestSet+(i+1)*lengthOfSequences])
    testSetSplitGarbeled.append( garble(testSetSplit[-1],testGarbleProb) )
    testSetGarbPofH1.append( pOutputSequence(testSetSplitGarbeled[-1],letters,transition_dictLog,testGarbleProb)  )

    bkgSample = ''
    for j in range(lengthOfSequences):
        bkgSample+= letters[random.randint(0,len(letters)-1)]
    bkgSetPofH1.append( pOutputSequence(bkgSample,letters,transition_dictLog,testGarbleProb) )


endtime = datetime.datetime.now()
print 'tests done : '+str(endtime-starttime)

np.save( 'testfile.npy', [ testSetGarbPofH1 , bkgSetPofH1  ])


