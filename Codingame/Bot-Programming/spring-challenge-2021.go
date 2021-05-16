// TODO
// spooky shadow

package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"math/rand"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

const MAX_ROUNDS = 24
const MAP_RING_COUNT = 3

const RICHNESS_NULL = 0
const RICHNESS_POOR = 1
const RICHNESS_OK = 2
const RICHNESS_LUSH = 3

const TREE_NONE = -1
const TREE_SEED = 0
const TREE_SMALL = 1
const TREE_MEDIUM = 2
const TREE_TALL = 3

var TREE_BASE_COST = [4]int{0, 1, 3, 7}

const TREE_COST_SCALE = 1
const LIFECYCLE_END_COST = 4
const DURATION_ACTION_PHASE = 1000
const DURATION_GATHER_PHASE = 2000
const DURATION_SUNMOVE_PHASE = 1000
const STARTING_TREE_COUNT = 2
const RICHNESS_BONUS_OK = 2
const RICHNESS_BONUS_LUSH = 4

func Error(a ...interface{}) {
	fmt.Fprintln(os.Stderr, a)
}

func Max(x, y int) int {
	if x < y {
		return y
	}
	return x
}

func Min(x, y int) int {
	if x > y {
		return y
	}
	return x
}

func IndexOf(element interface{}, data []interface{}) int {
	for k, v := range data {
		if element == v {
			return k
		}
	}
	return -1 //not found.
}

var directions = [][]int{{1, -1, 0}, {+1, 0, -1}, {0, +1, -1}, {-1, +1, 0}, {-1, 0, +1}, {0, -1, +1}}

type CubeCoord struct {
	X int
	Y int
	Z int
}

func (c *CubeCoord) Neighbor(orientation int) CubeCoord {
	return c.NeighborByDistance(orientation, 1)
}

func (c *CubeCoord) NeighborByDistance(orientation, distance int) CubeCoord {
	return CubeCoord{
		c.X + directions[orientation][0]*distance,
		c.Y + directions[orientation][1]*distance,
		c.Z + directions[orientation][2]*distance,
	}
}

func (a *CubeCoord) Add(b CubeCoord) CubeCoord {
	return CubeCoord{a.X + b.X, a.Y + b.Y, a.Z + b.Z}
}

func newCubeCoord(x, y, z int) CubeCoord {
	return CubeCoord{x, y, z}
}

type Cell struct {
	Index     int
	Richness  int // min: 1, max: 3
	Neighbors []int
}

type Tree struct {
	CellID  int
	Size    int // size -1 = no tree
	OwnerID int // ownerID -1 = no tree
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

func (a *Action) String() string {
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
	JustMovedPlayerId int // Who just moved, if they took the last chip they win.
	ActivePlayerId    int // This is the player who's current turn it is.

	// current game state from input
	Day             int
	Nutrients       int
	PossibleActions []*Action
	Trees           []*Tree   // tree is index by cell ID
	Players         []*Player // player 0 is me and 1 is opponent

	// hidden game state
	DyingTrees     []int
	Shadows        map[int]int
	SunOrientation int
}

func (game *Game) move() {
	// the constant biasing exploitation vs exploration
	var ucbC float64 = 1.0
	// Timeout to simulate in nanosec
	var timeout int64 = 95000000 // 95ms
	// How many simulations do players make when valuing the new moves?
	var simulations uint = 100 * MAX_ROUNDS

	// Run the simulation
	var move Move = Uct(game, timeout, simulations, ucbC, 0, evalScore)
	fmt.Println(move.(*Action).String())
	return
}

// evalScore evaluation scores the game state from a player's perspective, returning 0.0 (lost), 0.5 (in progress), 1.0 (won)
func evalScore(playerID int, state GameState) float64 {
	// TODO evaluation score
	var g *Game = state.(*Game)

	// Error(g.Players[0].Score, g.Players[0].Sun, g.Players[1].Score, g.Players[1].Sun)

	return float64((g.Players[0].Score + g.Players[0].Sun/3) - (g.Players[1].Score + g.Players[1].Sun/3))
}

func getOpponentId(playerID int) int {
	if playerID == 1 {
		return 0
	}
	return 1
}

// Clone makes a deep copy of the game state.
func (g *Game) Clone() GameState {
	newGame := &Game{
		JustMovedPlayerId: g.JustMovedPlayerId,
		ActivePlayerId:    g.ActivePlayerId,
		Day:               g.Day,
		Nutrients:         g.Nutrients,
		DyingTrees:        g.DyingTrees,
		Shadows:           g.Shadows,
		SunOrientation:    g.SunOrientation,
	}

	newGame.Trees = make([]*Tree, numberOfCells)
	for i, v := range g.Trees {
		newGame.Trees[i] = &Tree{
			CellID:  v.CellID,
			Size:    v.Size,
			OwnerID: v.OwnerID,
			Dormant: v.Dormant,
		}
	}
	newGame.Players = make([]*Player, 2)
	for i, v := range g.Players {
		newGame.Players[i] = &Player{
			Sun:   v.Sun,
			Score: v.Score,
		}
	}

	newGame.PossibleActions = make([]*Action, len(g.PossibleActions))
	for i, v := range g.PossibleActions {
		newGame.PossibleActions[i] = &Action{
			Type:       v.Type,
			TargetCell: v.TargetCell,
			SourceCell: v.SourceCell,
		}
	}

	return newGame
}

func (g *Game) updatePossibleAction() {
	var activePlayerID = g.ActivePlayerId
	g.PossibleActions = nil

	if g.Day > MAX_ROUNDS { // No move if the game end
		return
	}

	g.PossibleActions = append(g.PossibleActions, &Action{ActionTypeWait, 0, 0}) // add wait

	// For each tree, where they can seed.
	// For each tree, if they can grow.
	var seedCost = g.getCostFor(0, activePlayerID)
	for _, tree := range g.Trees {
		if tree.OwnerID == activePlayerID {
			var coord = Coords[tree.CellID]
			if g.playerCanSeedFrom(activePlayerID, tree, seedCost) {
				for _, targetCoord := range g.getCoordsInRange(coord, tree.Size) {
					targetCell := CoordCellMaps[targetCoord]
					if g.playerCanSeedTo(targetCell) {
						g.PossibleActions = append(g.PossibleActions, &Action{ActionTypeSeed, targetCell.Index, tree.CellID})
					}
				}
			}

			growCost := g.getGrowthCost(tree)
			if growCost <= g.Players[activePlayerID].Sun && !tree.Dormant {
				if tree.Size == TREE_TALL {
					g.PossibleActions = append(g.PossibleActions, &Action{ActionTypeComplete, tree.CellID, 0})
				} else {
					g.PossibleActions = append(g.PossibleActions, &Action{ActionTypeGrow, tree.CellID, 0})
				}
			}
		}
	}
}

// AvailableMoves returns all the available moves.
func (g *Game) AvailableMoves() []Move {
	var moves []Move // MCTS move availables

	for _, a := range g.PossibleActions {
		moves = append(moves, a)
	}

	return moves
}

// MakeMove makes a move in the game state, changing it.
func (g *Game) MakeMove(move Move) {
	// Convert the move to a form we can use.
	var action *Action = move.(*Action)

	// do action to update game state
	g.doAction(action)

	if action.Type == ActionTypeWait {
		g.updatePlayerTurn()

		// Update round
		if g.JustMovedPlayerId == 1 {
			g.removeDyingTrees()
			g.performSunMoveUpdate()
			g.performSunGatheringUpdate()
		}
	}

	g.updatePossibleAction()
}

func (g *Game) updatePlayerTurn() {
	g.JustMovedPlayerId = g.ActivePlayerId
	g.ActivePlayerId = getOpponentId(g.ActivePlayerId)
}

func (g *Game) setSunOrientation(orientation int) {
	g.SunOrientation = orientation % 6
}

func (g *Game) moveSunOrientation() {
	g.SunOrientation = (g.SunOrientation + 1) % 6
}

func (g *Game) calculateShadows() {
	// Clear shadows
	g.Shadows = make(map[int]int)
	for _, tree := range g.Trees {
		if tree.Size != TREE_NONE {
			var coord = Coords[tree.CellID]
			for i := 1; i <= tree.Size; i++ {
				var tempCoord = coord.NeighborByDistance(g.SunOrientation, i)
				var cell = CoordCellMaps[tempCoord]
				if cell != nil {
					g.Shadows[cell.Index] = Max(g.Shadows[cell.Index], tree.Size)
				}
			}
		}
	}
}

func (g *Game) performSunGatheringUpdate() {
	for _, tree := range g.Trees {
		tree.Dormant = false
		if tree.OwnerID != TREE_NONE {
			if g.Shadows[tree.CellID] == 0 || g.Shadows[tree.CellID] < tree.Size {
				g.Players[tree.OwnerID].Sun += tree.Size
			}
		}
	}
}

func (g *Game) performSunMoveUpdate() {
	g.Day++
	if g.Day < MAX_ROUNDS {
		g.moveSunOrientation()
		g.calculateShadows()
	}
}

func (g *Game) removeDyingTrees() {
	for _, dyingTreeIdx := range g.DyingTrees {
		var cell = Cells[dyingTreeIdx]
		var dyingTree = g.Trees[dyingTreeIdx]
		var points = g.Nutrients
		if cell.Richness == RICHNESS_OK {
			points += RICHNESS_BONUS_OK
		} else if cell.Richness == RICHNESS_LUSH {
			points += RICHNESS_BONUS_LUSH
		}

		g.Players[dyingTree.OwnerID].Score += points

		// remove tree
		g.Trees[dyingTreeIdx] = &Tree{dyingTreeIdx, TREE_NONE, -1, false}

		// update nutrients
		g.Nutrients = Max(0, g.Nutrients-1)
	}
	// Clear dying tree
	g.DyingTrees = []int{}
}

// DoAction to update game state
func (g *Game) doAction(action *Action) {
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
	var targetTree *Tree = g.Trees[action.TargetCell]

	g.Players[g.ActivePlayerId].Sun -= g.getGrowthCost(targetTree)

	g.DyingTrees = append(g.DyingTrees, targetTree.CellID)

	targetTree.Dormant = true
}

func (g *Game) doSeed(action *Action) {
	var sourceTree = g.Trees[action.SourceCell]
	sourceTree.Dormant = true

	g.Players[g.ActivePlayerId].Sun -= g.getCostFor(0, g.ActivePlayerId)
	g.Trees[action.TargetCell] = &Tree{action.TargetCell, TREE_SEED, g.ActivePlayerId, true}
}

func (g *Game) playerCanSeedFrom(playerID int, tree *Tree, seedCost int) bool {
	return seedCost <= g.Players[playerID].Sun && tree.Size > TREE_SEED && !tree.Dormant
}

func (g *Game) playerCanSeedTo(cell *Cell) bool {
	return cell != nil && cell.Richness != RICHNESS_NULL && g.Trees[cell.Index].Size == TREE_NONE
}

func (g *Game) doGrow(action *Action) {
	var targetTree *Tree = g.Trees[action.TargetCell]
	g.Players[g.ActivePlayerId].Sun -= g.getGrowthCost(g.Trees[action.TargetCell])

	targetTree.Size += 1
	targetTree.Dormant = true
}

func (g *Game) getGrowthCost(targetTree *Tree) int {
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

// Global variable
var game Game
var numberOfCells int
var Cells []*Cell
var Coords []CubeCoord // TODO test this
var CoordCellMaps map[CubeCoord]*Cell
var cellIndex = 0

func generateCell(coord CubeCoord, richness int) {
	Coords[cellIndex] = coord
	CoordCellMaps[coord] = Cells[cellIndex]
	// Error(cellIndex, Coords[cellIndex], CoordCellMaps[coord], Cells[cellIndex], Cells[cellIndex].Neighbors)
	cellIndex++
}

func generateCoords() {
	centre := CubeCoord{0, 0, 0}
	generateCell(centre, RICHNESS_LUSH)

	coord := centre.Neighbor(0)

	for distance := 1; distance <= MAP_RING_COUNT; distance++ {
		for orientation := 0; orientation < 6; orientation++ {
			for count := 0; count < distance; count++ {
				if distance == MAP_RING_COUNT {
					generateCell(coord, RICHNESS_POOR)
				} else if distance == MAP_RING_COUNT-1 {
					generateCell(coord, RICHNESS_OK)
				} else {
					generateCell(coord, RICHNESS_LUSH)
				}
				coord = coord.Neighbor((orientation + 2) % 6)
			}
		}
		coord = coord.Neighbor(0)
	}
}

func (g *Game) getCoordsInRange(center CubeCoord, N int) []CubeCoord {
	var results []CubeCoord
	for x := -N; x <= +N; x++ {
		for y := Max(-N, -x-N); y <= Min(+N, -x+N); y++ {
			results = append(results, center.Add(CubeCoord{x, y, -x - y}))
		}
	}
	return results
}

func main() {
	// rand.Seed(1)

	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1000000), 1000000)

	scanner.Scan()
	fmt.Sscan(scanner.Text(), &numberOfCells)

	game.ActivePlayerId = 0
	game.JustMovedPlayerId = 1

	Cells = make([]*Cell, numberOfCells)
	Coords = make([]CubeCoord, numberOfCells)
	CoordCellMaps = make(map[CubeCoord]*Cell)

	game.Nutrients = 20
	game.Trees = make([]*Tree, numberOfCells) // tree index by cellIndex and size by numberOfCells

	for i := 0; i < numberOfCells; i++ {
		var index, richness, neigh0, neigh1, neigh2, neigh3, neigh4, neigh5 int
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &index, &richness, &neigh0, &neigh1, &neigh2, &neigh3, &neigh4, &neigh5)

		Cells[index] = &Cell{
			index,
			richness,
			[]int{
				neigh0, neigh1, neigh2, neigh3, neigh4, neigh5,
			},
		}
		game.Trees[index] = &Tree{index, TREE_NONE, -1, false} // initial tree
	}

	generateCoords()
	game.Players = make([]*Player, 2)
	game.Players[0] = &Player{}
	game.Players[1] = &Player{}

	for {
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &game.Day)
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &game.Nutrients)
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &game.Players[0].Sun, &game.Players[0].Score)

		scanner.Scan()
		var _oppIsWaiting int
		fmt.Sscan(scanner.Text(), &game.Players[1].Sun, &game.Players[1].Score, &_oppIsWaiting)

		var numberOfTrees int
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &numberOfTrees)

		// Reset trees
		for i := 0; i < numberOfCells; i++ {
			game.Trees[i] = &Tree{i, TREE_NONE, -1, false} // initial tree
		}

		for i := 0; i < numberOfTrees; i++ {
			var cellIndex, size int
			var isDormant bool
			var _isMine, _isDormant, ownerID int
			scanner.Scan()
			fmt.Sscan(scanner.Text(), &cellIndex, &size, &_isMine, &_isDormant)
			ownerID = getOpponentId(_isMine)
			isDormant = _isDormant != 0

			game.Trees[cellIndex] = &Tree{cellIndex, size, ownerID, isDormant}
		}

		var numberOfPossibleMoves int
		scanner.Scan()
		fmt.Sscan(scanner.Text(), &numberOfPossibleMoves)

		game.PossibleActions = make([]*Action, numberOfPossibleMoves)
		for i := 0; i < numberOfPossibleMoves; i++ {
			scanner.Scan()
			possibleMove := scanner.Text()
			toks := strings.Split(possibleMove, " ")
			action := &Action{toks[0], 0, 0}
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
			game.PossibleActions[i] = action
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
type Scorer func(playerId int, state GameState) float64

type nilMove struct{}

func (n nilMove) Probability() float64 {
	return 0.0
}

// Uct is an Upper Confidence Bound Tree search through game stats for an optimal move, given a starting game state.
func Uct(state GameState, timeout int64, simulations uint, ucbC float64, playerId int, scorer Scorer) Move {

	// Find the best move given a fixed number of state explorations.
	var root *treeNode = newTreeNode(nil, nilMove{}, state, ucbC)
	var startTime = time.Now().UnixNano()
	var sim = 0
	var iter = 0
	for {
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
			sim++
		}

		// Backpropagate.
		// Our simulated state may be good or bad in the eyes of our player of interest.
		var outcome float64 = scorer(playerId, simulatedState)
		node.addOutcome(outcome) // Will internally propogate up the tree.
		if time.Now().UnixNano()-startTime > timeout {
			break
		}
		iter++
	}
	Error(iter, sim)

	// The best move to take is going to be the root nodes most visited child.
	sort.Sort(byVisits(root.children))

	lasIdx := len(root.children) - 1
	var g = root.children[lasIdx].state.(*Game)
	var bestScore = evalScore(0, root.children[lasIdx].state)
	Error(bestScore, g.Players[0].Score, g.Players[0].Sun, g.Players[1].Score, g.Players[1].Sun)

	return root.children[0].move // Descending by visits.
}

func upperConfidenceBound(childAggregateOutcome float64, ucbC float64, parentVisits uint64, childVisits uint64) float64 {
	return childAggregateOutcome/float64(childVisits) + ucbC*math.Sqrt(2*math.Log(float64(parentVisits))/float64(childVisits))
}
