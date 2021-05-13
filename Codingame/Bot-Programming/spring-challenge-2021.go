package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"math"
	"math/rand"
	"os"
	"sort"
	"strconv"
	"strings"
)

var TREE_SEED = 0
var TREE_SMALL = 1
var TREE_MEDIUM = 2
var TREE_TALL = 3
var TREE_BASE_COST = [4]int{0, 1, 3, 7}
var LIFECYCLE_END_COST = 4

type Cell struct {
	Index     int
	Richness  int // min: 1, max: 3
	Neighbors []int
}

type Tree struct {
	CellId  int
	Size    int
	OwnerID int
	Dormant bool
}

const ActionTypeComplete = "COMPLETE"
const ActionTypeGrow = "GROW"
const ActionTypeSeed = "SEED"
const ActionTypeWait = "WAIT"

type Action struct {
	Type       string
	TargetCell int
	SourceCell int
}

func (a Action) String() string {
	switch a.Type {
	case ActionTypeWait:
		return "WAIT"
	case ActionTypeSeed:
		return fmt.Sprintf("SEED %d %d", a.SourceCell, a.TargetCell)
	default:
		return fmt.Sprintf("%s %d", a.Type, a.TargetCell)
	}
}

// Probability() indicates the probability of the move if it can only occur in rare conditions (say with a dice outcome)
func (a *Action) Probability() float64 {
	return 1.0 // No randomness
}

type Player struct {
	Sun   int
	Score int
}

type Game struct {
	// Public members are used by the scoring function and running the game.
	JustMovedPlayerId uint64 // Who just moved, if they took the last chip they win.
	ActivePlayerId    uint64 // This is the player who's current turn it is.

	// current game state from input
	Day               int
	Nutrients         int
	Board             []Cell
	MyPossibleActions []Action
	Trees             []Tree   // tree is index by cell ID
	Players           []Player // player 0 is me and 1 is opponent
	OpponentIsWaiting bool

	// hidden game state
	DyingTrees []Tree
}

func (game *Game) move() {
	// the constant biasing exploitation vs exploration
	var ucbC float64 = 1.0
	// How many iterations do players take when considering moves?
	var iterations uint = 1000
	// How many simulations do players make when valuing the new moves?
	var simulations uint = 100

	// Run the simulation
	var move Move = Uct(game, iterations, simulations, ucbC, 1, evalScore)
	fmt.Println(move.(*Action).String())
	return
}

// evalScore evaluation scores the game state from a player's perspective, returning 0.0 (lost), 0.5 (in progress), 1.0 (won)
func evalScore(playerID uint64, state GameState) float64 {
	// TODO score
	return 0.5
}

// Clone makes a deep copy of the game state.
func (g *Game) Clone() GameState {
	newGame := &Game{}
	byt, _ := json.Marshal(g)
	json.Unmarshal(byt, newGame)
	return newGame
}

// AvailableMoves returns all the available moves.
func (g *Game) AvailableMoves() []Move {
	var moves []Move
	// TODO get all avaliable moves
	return moves
}

// MakeMove makes a move in the game state, changing it.
func (g *Game) MakeMove(move Move) {
	// Convert the move to a form we can use.
	var action *Action = move.(*Action)

	// do action to update game state
	g.doAction(action)

	g.updatePlayerTurn()
}

func (g *Game) updatePlayerTurn() {
	g.JustMovedPlayerId = g.ActivePlayerId
	// There are only two players so whichever player is not active should be the new active player.
	if g.ActivePlayerId == 0 {
		g.ActivePlayerId = 1
		return
	}
	g.ActivePlayerId = 0
}

// RandomizeUnknowns has no effect since Nim has no random hidden information.
func (g *Game) RandomizeUnknowns() {}

// DoAction to update game state
func (g *Game) doAction(action *Action) {
	// TODO change game state by action
	switch action.Type {
	case ActionTypeGrow:
		g.doGrow(action)
		return
	case ActionTypeSeed:
		g.doSeed(action)
		return
	case ActionTypeComplete:
		g.doComplete(action)
		return
	default:
	}
}

func (g *Game) doComplete(action *Action) {
	var targetTree = g.Trees[action.TargetCell]

	var costOfGrowth = g.getGrowthCost(targetTree)
	g.Players[g.ActivePlayerId].Sun -= costOfGrowth

	// TODO add dying tree
	targetTree.Dormant = true
}

func (g *Game) doSeed(action *Action) {
	var sourceTree = g.Trees[action.SourceCell]

	var costOfSeed = g.getCostFor(0, int(g.ActivePlayerId))
	g.Players[g.ActivePlayerId].Sun -= costOfSeed

	sourceTree.Dormant = true
	g.Trees[action.TargetCell] = Tree{action.TargetCell, TREE_SEED, int(g.ActivePlayerId), false}
}

func (g *Game) doGrow(action *Action) {
	var targetTree Tree = g.Trees[action.TargetCell]

	var costOfGrowth = g.getGrowthCost(targetTree)
	g.Players[g.ActivePlayerId].Sun -= costOfGrowth

	targetTree.Size += 1
	targetTree.Dormant = true
}

func (g *Game) getGrowthCost(targetTree Tree) int {
	var targetSize = targetTree.Size + 1
	if targetSize > TREE_TALL { // target > max size
		return LIFECYCLE_END_COST // end tree cost is 4
	}
	return g.getCostFor(targetSize, targetTree.OwnerID)
}

func (g *Game) getCostFor(size, ownerID int) int {
	var baseCost = TREE_BASE_COST[size]
	var sameTreeCount = 0
	for _, tree := range g.Trees {
		if tree.Size == size && tree.OwnerID == ownerID {
			sameTreeCount += 1
		}
	}
	return baseCost + sameTreeCount
}

var game Game

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1000000), 1000000)

	var numberOfCells int
	scanner.Scan()
	fmt.Sscan(scanner.Text(), &numberOfCells)

	game.ActivePlayerId = 0
	game.JustMovedPlayerId = 1

	game.Nutrients = 20
	game.Board = make([]Cell, numberOfCells)
	game.Trees = make([]Tree, numberOfCells) // tree index by cellIndex and size by numberOfCells
	game.DyingTrees = []Tree{}

	for i := 0; i < numberOfCells; i++ {
		var index, richness, neigh0, neigh1, neigh2, neigh3, neigh4, neigh5 int
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &index, &richness, &neigh0, &neigh1, &neigh2, &neigh3, &neigh4, &neigh5)

		game.Board[i] = Cell{
			index,
			richness,
			[]int{
				neigh0, neigh1, neigh2, neigh3, neigh4, neigh5,
			},
		}
	}
	for {
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &game.Day)
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &game.Nutrients)
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &game.Players[0].Sun, &game.Players[0].Score)

		scanner.Scan()
		var _oppIsWaiting int
		fmt.Sscan(scanner.Text(), &game.Players[1].Sun, &game.Players[1].Sun, &_oppIsWaiting)
		game.OpponentIsWaiting = _oppIsWaiting != 0

		var numberOfTrees int
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &numberOfTrees)

		for i := 0; i < numberOfTrees; i++ {
			var cellIndex, size int
			var isDormant bool
			var _isMine, _isDormant, ownerID int
			scanner.Scan()
			fmt.Sscan(scanner.Text(), &cellIndex, &size, &_isMine, &_isDormant)
			ownerID = int(math.Abs(float64(_isMine - 1)))
			isDormant = _isDormant != 0

			game.Trees[cellIndex] = Tree{cellIndex, size, ownerID, isDormant}
		}

		var numberOfPossibleMoves int
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &numberOfPossibleMoves)

		game.MyPossibleActions = make([]Action, numberOfPossibleMoves)
		for i := 0; i < numberOfPossibleMoves; i++ {
			scanner.Scan()
			possibleMove := scanner.Text()
			toks := strings.Split(possibleMove, " ")
			action := Action{toks[0], 0, 0}
			switch toks[0] {
			case "COMPLETE":
				action.TargetCell, _ = strconv.Atoi(toks[1])
			case "GROW":
				action.TargetCell, _ = strconv.Atoi(toks[1])
			case "SEED":
				action.SourceCell, _ = strconv.Atoi(toks[1])
				action.TargetCell, _ = strconv.Atoi(toks[2])
			case "WAIT":
				_ = ""
			default:
				panic(fmt.Sprintf("Unexpected action '%s'.", toks[0]))
			}
			game.MyPossibleActions[i] = action
		}

		game.move()
	}
}

// ----------------- MCTS -----------------

// Move represents a move in the game.
type Move interface {
	Probability() float64 // If this this move has random components indicate the chance it takes place (0.0-1.0).
}

// GameState is the interface a game supports to satisfy the MCTS.
type GameState interface {
	Clone() GameState       // Clone the game state, a deep copy.
	AvailableMoves() []Move // Return all the viable moves given the current game state. For a finished game, nil.
	MakeMove(move Move)     // Take an action, changing the game state.
	RandomizeUnknowns()     // Any game state that is unknown (like order of cards), randomize.
}

// A node in the (action, state) game tree. Wins are from the veiwpoint of the player-just-moved.
type treeNode struct {
	parent         *treeNode   // What node contains this node? Root node's parent is nil.
	move           Move        // What move lead to this node? Root node's action is nil.
	state          GameState   // What is the game state at this node?
	totalOutcome   float64     // What is the sum of all outcomes computed for this node and its children? From the point of view of a single player.
	probability    float64     // The probability of this move even occuring (when it involes randomness) as 0.0-1.0.
	visits         uint64      // How many times has this node been studied? Used with totalValue to compute an average value for the node.
	untriedMoves   []Move      // What moves have not yet been explored from this state?
	children       []*treeNode // The children of this node, can be many.
	ucbC           float64     // The UCB constant used in selection calcualtions.
	selectionScore float64     // The computed score for this node used in selection, balanced between exploitation and exploration.
}

// newTreeNode creates a new well-formed tree node.
func newTreeNode(parent *treeNode, move Move, state GameState, ucbC float64) *treeNode {

	// Sanity check the move probability.
	var probability float64 = move.Probability()
	if probability < 0.0 || probability > 1.0 {
		log.Panicf("Move cannot have a probability outside of the range 0.0-1.0: %f", probability)
	}

	// Construct the new node.
	var node treeNode = treeNode{
		parent:         parent,
		move:           move,
		state:          state,
		totalOutcome:   0.0,                    // No outcome yet.
		probability:    probability,            // Some moves happen so rarely we want to weight the value of their influence.
		visits:         0,                      // No visits yet.
		untriedMoves:   state.AvailableMoves(), // Initially the node starts with every node unexplored.
		children:       nil,                    // No children yet.
		ucbC:           ucbC,                   // Whole tree uses same constant.
		selectionScore: 0.0,                    // No valute yet.
	}

	// We're working with pointers.
	return &node
}

// getVisits returns the visits to a node, 0 if the node doesn't exist (for when a root checks its parent).
func (n *treeNode) getVisits() uint64 {
	if n == nil {
		return 0
	}
	return n.visits
}

// computeSelectionScore prepares the selection score of a single child.
func (n *treeNode) computeSelectionScore() {
	n.selectionScore = upperConfidenceBound(n.totalOutcome, n.ucbC, n.parent.getVisits(), n.visits)
}

// selectChild picks the child with the highest selection score (balancing exploration and exploitation).
func (n *treeNode) selectChild() *treeNode {
	// Sort the children by their UCB, balances winning children with unexplored children.
	sort.Sort(bySelectionScore(n.children))
	return n.children[0]
}

// addOutcome adds the outcome value from a computation involving the node or one of its children.
// Every outcome value in the tree is from the perspective of a particular player. Higher outcomes mean better
// winning situations for the player.
func (n *treeNode) addOutcome(outcome float64) {
	// Allow the root to call this on its parent with no ill effect.
	if n != nil {
		// Some nodes are so unlikely to be visited, the outcome should be weighted.
		var weightedOutcome float64 = outcome * n.probability
		// Update this node's data.
		n.totalOutcome += weightedOutcome
		n.visits++
		// Pass the value up to the parent as well.
		n.parent.addOutcome(weightedOutcome) // Will recurse up the tree to the root.
		// Now that the parent is also updated
		n.computeSelectionScore()
	}
}

// makeRandomUntriedMove makes a random untried move and builds another node in the tree from the result.
func (n *treeNode) makeRandomUntriedMove() *treeNode {

	// Select a random move we haven't tried.
	var i int = rand.Intn(len(n.untriedMoves))
	var move Move = n.untriedMoves[i]

	// Remove it from the untried moves.
	n.untriedMoves = append(n.untriedMoves[:i], n.untriedMoves[i+1:]...)

	// Clone the node's state so we don't alter it.
	var newState GameState = n.state.Clone()
	newState.MakeMove(move)

	// Build more of the tree.
	var child *treeNode = newTreeNode(n, move, newState, n.ucbC)
	n.children = append(n.children, child) // End of children list are the children with lowest selection scores (e.g. no visits).

	// Return a game state that can be used for simulations.
	return child
}

// bySelectionScore implements sort.Interface to sort *descending* by selection score.
// Example: sort.Sort(bySelectionScore(nodes))
type bySelectionScore []*treeNode

func (a bySelectionScore) Len() int           { return len(a) }
func (a bySelectionScore) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a bySelectionScore) Less(i, j int) bool { return a[i].selectionScore > a[j].selectionScore }

// byVisits implements sort.Interface to sort *descending* by visits.
// Example: sort.Sort(byVisits(nodes))
type byVisits []*treeNode

func (a byVisits) Len() int           { return len(a) }
func (a byVisits) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a byVisits) Less(i, j int) bool { return a[i].visits > a[j].visits }

// Scorer is the function an AI can use to just the benifit of an outcome from the eyes of a particular player.
type Scorer func(playerId uint64, state GameState) float64

// Uct is an Upper Confidence Bound Tree search through game stats for an optimal move, given a starting game state.
func Uct(state GameState, iterations uint, simulations uint, ucbC float64, playerId uint64, scorer Scorer) Move {

	// Find the best move given a fixed number of state explorations.
	var root *treeNode = newTreeNode(nil, nil, state, ucbC)
	for i := 0; i < int(iterations); i++ {

		// Start at the top of the tree again.
		var node *treeNode = root

		// Select. Find the node we wish to explore next.
		// While we have complete nodes, dig deeper for a new state to explore.
		for len(node.untriedMoves) == 0 && len(node.children) > 0 {
			// This node has no more moves to try but it does have children.
			// Move the focus to its most promising child.
			node = node.selectChild()
		}

		// Expand.
		// Can we explore more about this particular state? Are there untried moves?
		if len(node.untriedMoves) > 0 {
			node = node.makeRandomUntriedMove() // This creates a new child node with cloned game state.
		}

		// Simulation.
		// From the new child, make many simulated random steps to get a fuzzy idea of how good
		// the move that created the child is.
		var simulatedState GameState = node.state.Clone()
		for j := 0; j < int(simulations); j++ {
			// Randomize any part of the game state that is unkonwn to all the players (e.g. facedown cards).
			simulatedState.RandomizeUnknowns()
			// What moves can further the game state?
			var availableMoves []Move = simulatedState.AvailableMoves()
			// Is the game over?
			if len(availableMoves) == 0 {
				break
			}
			// Pick a random move (could be any player).
			var randomIndex int = rand.Intn(len(availableMoves))
			var move Move = availableMoves[randomIndex]
			simulatedState.MakeMove(move)
		}

		// Backpropagate.
		// Our simulated state may be good or bad in the eyes of our player of interest.
		var outcome float64 = scorer(playerId, simulatedState)
		node.addOutcome(outcome) // Will internally propogate up the tree.
	}

	// The best move to take is going to be the root nodes most visited child.
	sort.Sort(byVisits(root.children))
	return root.children[0].move // Descending by visits.
}

func upperConfidenceBound(childAggregateOutcome float64, ucbC float64, parentVisits uint64, childVisits uint64) float64 {
	return childAggregateOutcome/float64(childVisits) + ucbC*math.Sqrt(2*math.Log(float64(parentVisits))/float64(childVisits))
}
