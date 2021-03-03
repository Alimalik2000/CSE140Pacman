import random
from pacai.bin import capture
from pacai.util import reflection
from pacai.agents.capture.capture import CaptureAgent

class QuantumSlugAgent(CaptureAgent):
    def __init__(self, index, timeForComputing = 0.1):
        super().__init__(index, timeForComputing)

    def chooseAction(self, gameState):
        legalActions = gameState.getLegalActions(self.index)
        return random.choice(legalActions)

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

    firstAgent = QuantumSlugAgent
    secondAgent = QuantumSlugAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]
