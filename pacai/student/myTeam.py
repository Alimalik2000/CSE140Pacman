import random
import random
import time
from pacai.bin import capture
from pacai.bin import capture
from pacai.util import reflection
from pacai.agents.capture.capture import CaptureAgent
from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.core.directions import Directions
from pacai.util import counter
import abc

from pacai.agents.base import BaseAgent
from pacai.core import distanceCalculator
from pacai.util import util


class QuantumCaptureAgent(CaptureAgent):
    """
    A base class for reflex agents that chooses score-maximizing actions.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the agent and populates useful fields,
        such as the team the agent is on and the `pacai.core.distanceCalculator.Distancer`.
        """

        self.red = gameState.isOnRedTeam(self.index)
        self.distancer = distanceCalculator.Distancer(gameState.getInitialLayout())

        self.distancer.getMazeDistances()

    def final(self, gameState):
        self.observationHistory = []

    def registerTeam(self, agentsOnTeam):
        """
        Fills the self.agentsOnTeam field with a list of the
        indices of the agents on your team.
        """

        self.agentsOnTeam = agentsOnTeam

    def getAction(self, gameState):
        self.observationHistory.append(gameState)

        myState = gameState.getAgentState(self.index)
        myPos = myState.getPosition()

        if (myPos != util.nearestPoint(myPos)):
            # We're halfway from one position to the next.
            return gameState.getLegalActions(self.index)[0]
        else:
            return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest return from `ReflexCaptureAgent.evaluate`.
        """

        actions = gameState.getLegalActions(self.index)

        
        values = [self.evaluate(gameState, a) for a in actions]
        

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        return random.choice(bestActions)

    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """

        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()

        if (pos != util.nearestPoint(pos)):
            # Only half a grid position was covered.
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights.
        """

        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)

        return features * weights

    def getFeatures(self, gameState, action):
        """
        Returns a dict of features for the state.
        The keys match up with the return from `ReflexCaptureAgent.getWeights`.
        """

        successor = self.getSuccessor(gameState, action)

        return {
            'successorScore': self.getScore(successor)
        }

    def getWeights(self, gameState, action):
        """
        Returns a dict of weights for the state.
        The keys match up with the return from `ReflexCaptureAgent.getFeatures`.
        """

        return {
            'successorScore': 1.0
        }

    def getFood(self, gameState):
        """
        Returns the food you're meant to eat.
        This is in the form of a `pacai.core.grid.Grid`
        where `m[x][y] = True` if there is food you can eat (based on your team) in that square.
        """

        if (self.red):
            return gameState.getBlueFood()
        else:
            return gameState.getRedFood()

    def getFoodYouAreDefending(self, gameState):
        """
        Returns the food you're meant to protect (i.e., that your opponent is supposed to eat).
        This is in the form of a `pacai.core.grid.Grid`
        where `m[x][y] = True` if there is food at (x, y) that your opponent can eat.
        """

        if (self.red):
            return gameState.getRedFood()
        else:
            return gameState.getBlueFood()

    def getCapsules(self, gameState):
        if (self.red):
            return gameState.getBlueCapsules()
        else:
            return gameState.getRedCapsules()

    def getCapsulesYouAreDefending(self, gameState):
        if (self.red):
            return gameState.getRedCapsules()
        else:
            return gameState.getBlueCapsules()

    def getOpponents(self, gameState):
        """
        Returns agent indices of your opponents. This is the list of the numbers
        of the agents (e.g., red might be 1, 3, 5)
        """

        if self.red:
            return gameState.getBlueTeamIndices()
        else:
            return gameState.getRedTeamIndices()

    def getTeam(self, gameState):
        """
        Returns agent indices of your team. This is the list of the numbers
        of the agents (e.g., red might be the list of 1,3,5)
        """

        if (self.red):
            return gameState.getRedTeamIndices()
        else:
            return gameState.getBlueTeamIndices()

    def getScore(self, gameState):
        """
        Returns how much you are beating the other team by in the form of a number
        that is the difference between your score and the opponents score.
        This number is negative if you're losing.
        """

        if (self.red):
            return gameState.getScore()
        else:
            return gameState.getScore() * -1

    def getMazeDistance(self, pos1, pos2):
        """
        Returns the distance between two points using the builtin distancer.
        """

        return self.distancer.getDistance(pos1, pos2)

    def getPreviousObservation(self):
        """
        Returns the `pacai.core.gamestate.AbstractGameState` object corresponding to
        the last state this agent saw.
        That is the observed state of the game last time this agent moved,
        this may not include all of your opponent's agent locations exactly.
        """

        if (len(self.observationHistory) <= 1):
            return None

        return self.observationHistory[-2]

    def getCurrentObservation(self):
        """
        Returns the GameState object corresponding this agent's current observation
        (the observed state of the game - this may not include
        all of your opponent's agent locations exactly).
        Returns the `pacai.core.gamestate.AbstractGameState` object corresponding to
        this agent's current observation.
        That is the observed state of the game last time this agent moved,
        this may not include all of your opponent's agent locations exactly.
        """

        if (len(self.observationHistory) == 0):
            return None

        return self.observationHistory[-1]


'''
Basic stub class that extends Capture agent
We need to implement choose action. Currently it just
returns a random legal action
'''
class OffenseQuantumSlugAgent(QuantumCaptureAgent):
    """
    A reflex agent that seeks food.
    This agent will give you an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """
    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = counter.Counter()
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)

        # Compute distance to the nearest food.
        foodList = self.getFood(successor).asList()

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        return features

    def getWeights(self, gameState, action):
        return {
            'successorScore': 100,
            'distanceToFood': -1
        }


class DefenseQuantumSlugAgent(QuantumCaptureAgent):
    """
    A reflex agent that tries to keep its side Pacman-free.
    This is to give you an idea of what a defensive agent could be like.
    It is not the best or only way to make such an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = counter.Counter()
        successor = self.getSuccessor(gameState, action)

        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        if (len(invaders) > 0):
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -10,
            'stop': -100,
            'reverse': -2
        }


def createTeam(firstIndex, secondIndex, isRed,
        first = 'pacai.agents.capture.dummy.DummyAgent',
        second = 'pacai.agents.capture.dummy.DummyAgent'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    # firstAgent = reflection.qualifiedImport(first)
    # secondAgent = reflection.qualifiedImport(second)

    firstAgent = OffenseQuantumSlugAgent
    secondAgent = DefenseQuantumSlugAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]
