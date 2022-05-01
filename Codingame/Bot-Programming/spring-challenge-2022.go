package main

// Anktinosia strategy
import (
	"fmt"
	"math"
	"os"
	"sort"
)

var baseX, baseY int

func Error(a ...interface{}) {
	fmt.Fprintln(os.Stderr, fmt.Sprintf("%v", a))
}

const (
	MonsterType = 0
	MyHeroType  = 1
	OpHeroType  = 2

	ThreatForNone   = 0
	ThreatForMyBase = 1
	ThreatForOpBase = 2

	BaseHit        = 300
	AttackerID     = 0
	AttackModeMana = 100 // All hero attack opponent base
	WindRange      = 2200
)

type Position struct {
	x int
	y int
}

type OpHero struct {
	id               int
	entityType       int
	x                int
	y                int
	shieldLife       int
	isControlled     int
	distanceToMyBase float64
	distanceToOpBase float64
}

type MyHero struct {
	id            int
	entityType    int
	x             int
	y             int
	shieldLife    int
	isControlled  int
	targetMonster *Monster
}

func (t MyHero) String() string {
	return fmt.Sprintf("{id:%v x:%v y:%v targetMonster:%v}", t.id, t.x, t.y, t.targetMonster)
}

type Monster struct {
	id               int
	entityType       int
	x                int
	y                int
	health           int
	vx               int
	vy               int
	nearBase         int
	threatFor        int
	shieldLife       int
	isControlled     int
	distanceToMyBase float64
	distanceToOpBase float64
}

func (t Monster) String() string {
	return fmt.Sprintf("{id:%v x:%v y:%v}", t.id, t.x, t.y)
}

func distance(x1, y1, x2, y2 int) float64 {
	return math.Sqrt(math.Pow(float64(y2)-float64(y1), 2) + math.Pow(float64(x2)-float64(x1), 2))
}

type MonsterByDistance []*Monster

func (m MonsterByDistance) Len() int { return len(m) }
func (m MonsterByDistance) Less(i, j int) bool {
	distance1 := m[i].distanceToMyBase
	// weight ThreatForMyBase
	// if m[i].threatFor != ThreatForMyBase {
	// 	distance1 *= 10000
	// }

	distance2 := m[j].distanceToMyBase
	// if m[j].threatFor != ThreatForMyBase {
	// 	distance2 *= 10000
	// }

	return distance1 < distance2
}
func (m MonsterByDistance) Swap(i, j int) { m[i], m[j] = m[j], m[i] }

type MonsterByOpBaseDistance []*Monster

func (m MonsterByOpBaseDistance) Len() int { return len(m) }
func (m MonsterByOpBaseDistance) Less(i, j int) bool {
	distance1 := m[i].distanceToOpBase
	// weight ThreatForOpBase
	// if m[i].threatFor != ThreatForOpBase {
	// 	distance1 *= 10000
	// }

	distance2 := m[j].distanceToOpBase
	// if m[j].threatFor != ThreatForOpBase {
	// 	distance2 *= 10000
	// }

	return distance1 < distance2
}
func (m MonsterByOpBaseDistance) Swap(i, j int) { m[i], m[j] = m[j], m[i] }

type OpHeroByDistance []*OpHero

func (m OpHeroByDistance) Len() int { return len(m) }
func (m OpHeroByDistance) Less(i, j int) bool {
	distance1 := m[i].distanceToMyBase
	distance2 := m[j].distanceToMyBase

	return distance1 < distance2
}
func (m OpHeroByDistance) Swap(i, j int) { m[i], m[j] = m[j], m[i] }

type OpHeroByOpBaseDistance []*OpHero

func (m OpHeroByOpBaseDistance) Len() int { return len(m) }
func (m OpHeroByOpBaseDistance) Less(i, j int) bool {
	distance1 := m[i].distanceToOpBase
	distance2 := m[j].distanceToOpBase

	return distance1 < distance2
}
func (m OpHeroByOpBaseDistance) Swap(i, j int) { m[i], m[j] = m[j], m[i] }

func main() {
	// baseX: The corner of the map representing your base
	fmt.Scan(&baseX, &baseY)

	var preparePosition []Position
	var attackPosition Position
	farmPosition := Position{
		x: 8815,
		y: 4500,
	}
	_ = farmPosition
	var opBaseX, opBaseY int
	_ = preparePosition
	if baseX < 8815 {
		preparePosition = []Position{
			{
				x: 4000,
				y: 4000,
			},
			{
				x: 1000,
				y: 6000,
			},
			{
				x: 6000,
				y: 1000,
			},
		}
		attackPosition = Position{
			x: 15500,
			y: 6900,
		}
		opBaseX, opBaseY = 17630, 9000
	} else {
		preparePosition = []Position{
			{
				x: 12000,
				y: 5000,
			},
			{
				x: 16000,
				y: 2000,
			},
			{
				x: 11000,
				y: 8000,
			},
		}
		opBaseX, opBaseY = 0, 0
		attackPosition = Position{
			// x: 2300,
			// y: 2000,
			x: 4900,
			y: 1000,
		}
	}

	// heroesPerPlayer: Always 3
	var heroesPerPlayer int
	fmt.Scan(&heroesPerPlayer)

	isAttackMode := false

	for {
		isFullAttackMode := false

		var myHealth, myMana int
		var opHealth, opMana int
		fmt.Scan(&myHealth, &myMana)
		fmt.Scan(&opHealth, &opMana)

		// entityCount: Amount of heros and monsters you can see
		var entityCount int
		fmt.Scan(&entityCount)

		var myHeroesSlice []*MyHero
		var opHeroesSlice []*OpHero
		var opHeroesSlice2 []*OpHero
		var monstersSlice []*Monster
		var monstersSlice2 []*Monster

		for i := 0; i < entityCount; i++ {
			// id: Unique identifier
			// type: 0=monster, 1=your hero, 2=opponent hero
			// x: Position of this entity
			// shieldLife: Ignore for this league; Count down until shield spell fades
			// isControlled: Ignore for this league; Equals 1 when this entity is under a control spell
			// health: Remaining health of this monster
			// vx: Trajectory of this monster
			// nearBase: 0=monster with no target yet, 1=monster targeting a base
			// threatFor: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
			var id, entityType, x, y, shieldLife, isControlled, health, vx, vy, nearBase, threatFor int
			fmt.Scan(&id, &entityType, &x, &y, &shieldLife, &isControlled, &health, &vx, &vy, &nearBase, &threatFor)

			switch entityType {
			case MyHeroType:
				myHeroesSlice = append(myHeroesSlice, &MyHero{
					id:           id,
					entityType:   entityType,
					x:            x,
					y:            y,
					shieldLife:   shieldLife,
					isControlled: isControlled,
				})
			case MonsterType:
				monster := Monster{
					id:               id,
					entityType:       entityType,
					x:                x,
					y:                y,
					health:           health,
					vx:               vx,
					vy:               vy,
					shieldLife:       shieldLife,
					isControlled:     isControlled,
					nearBase:         nearBase,
					threatFor:        threatFor,
					distanceToMyBase: distance(x, y, baseX, baseY),
					distanceToOpBase: distance(x, y, opBaseX, opBaseY),
				}
				monstersSlice = append(monstersSlice, &monster)
				monstersSlice2 = append(monstersSlice2, &monster)
			case OpHeroType:
				opHero := OpHero{
					id:               id,
					entityType:       entityType,
					x:                x,
					y:                y,
					shieldLife:       shieldLife,
					isControlled:     isControlled,
					distanceToMyBase: distance(x, y, baseX, baseY),
					distanceToOpBase: distance(x, y, opBaseX, opBaseY),
				}
				opHeroesSlice = append(opHeroesSlice, &opHero)
				opHeroesSlice2 = append(opHeroesSlice2, &opHero)
			default:
			}
		}

		if myMana > AttackModeMana {
			isAttackMode = true
		}
		if myMana > 100 || myHealth < opHealth {
			isFullAttackMode = true
		}

		// Defend mode
		sort.Sort(MonsterByDistance(monstersSlice))
		sort.Sort(MonsterByOpBaseDistance(monstersSlice2))
		sort.Sort(OpHeroByDistance(opHeroesSlice))
		sort.Sort(OpHeroByOpBaseDistance(opHeroesSlice2))

		if len(monstersSlice) > 0 {
			for _, monster := range monstersSlice {
				var closetHero *MyHero
				closetDistance := math.MaxFloat64
				for _, hero := range myHeroesSlice {
					if hero.targetMonster != nil {
						continue
					}
					dis := distance(monster.x, monster.y, hero.x, hero.y)
					if dis < closetDistance {
						closetHero = hero
						closetDistance = dis
					}
				}
				if closetHero != nil {
					closetHero.targetMonster = monster
				}
			}

			// Error(myHeroesSlice)

			for idx := 0; idx < heroesPerPlayer; idx++ {
				hero := myHeroesSlice[idx]
				if !isAttackMode || idx != AttackerID { //  2 defender
					if hero.targetMonster != nil && hero.targetMonster.distanceToMyBase < 10000 {
						if myMana >= 30 &&
							hero.targetMonster.shieldLife == 0 &&
							hero.targetMonster.distanceToMyBase < 6000 && // if monster inside near base 6000
							distance(hero.targetMonster.x, hero.targetMonster.y, hero.x, hero.y) < 1280 {
							fmt.Printf("SPELL WIND %d %d\n", opBaseX, opBaseY)
						} else {
							fmt.Printf("MOVE %d %d DefendMonster\n", hero.targetMonster.x, hero.targetMonster.y)
						}
					} else {
						if len(opHeroesSlice) > 0 { // follow opponent hero
							fmt.Printf("MOVE %d %d DefendHero\n", opHeroesSlice[0].x, opHeroesSlice[0].y)
						} else { // follow nearest monster
							fmt.Printf("MOVE %d %d DefendMonster\n", monstersSlice[0].x, monstersSlice[0].y)
						}
					}
				} else { // 1 attacker
					var shieldMonster *Monster
					var windMonster *Monster
					var attackMonster *Monster
					var controlHero *OpHero
					closeMonster := 0
					closetMonster := math.MaxFloat64
					// skill condition
					if isFullAttackMode {
						for _, opHero := range opHeroesSlice {
							if opHero.shieldLife == 0 &&
								distance(opHero.x, opHero.y, hero.x, hero.y) < 2200 &&
								opHero.distanceToOpBase < 6000 { // check no op in distance
								controlHero = opHero
							}
						}
						// for _, monster := range monstersSlice2 {
						// 	if monster.shieldLife == 0 && monster.threatFor == ThreatForOpBase &&
						// 	distance(monster.x, monster.y, hero.x, hero.y) < 2200 {
						// 		shieldMonster = monster
						// 		break
						// 	}
						// }
					}
					for _, monster := range monstersSlice2 {
						if isFullAttackMode && distance(monster.x, monster.y, hero.x, hero.y) < 1280 {
							closeMonster += 1
						}
						if isAttackMode && distance(monster.x, monster.y, hero.x, hero.y) < 1280 {
							if monster.distanceToOpBase < WindRange+BaseHit {
								// windMonster = monster
								isHeroClose := false
								for _, opHero := range opHeroesSlice {
									if opHero.shieldLife > 0 && distance(opHero.x, opHero.y, hero.x, hero.y) < 1280 { // check no op in distance
										isHeroClose = true
									}
								}
								if isHeroClose {
									shieldMonster = monster
								} else {
									windMonster = monster
								}
							}
						}
						if (!isAttackMode || monster.distanceToOpBase < 10000) && monster.shieldLife == 0 {
							dis := distance(monster.x, monster.y, hero.x, hero.y)
							if dis < closetMonster {
								attackMonster = monster
								closetMonster = dis
							}
						}
					}
					if myMana > 30 && windMonster != nil {
						fmt.Printf("SPELL WIND %d %d AttackWind\n", opBaseX, opBaseY)
					} else if myMana > 30 && shieldMonster != nil {
						fmt.Printf("SPELL SHIELD %d AttackShield\n", shieldMonster.id)
					} else if myMana > 30 && controlHero != nil {
						fmt.Printf("SPELL CONTROL %d %d %d AttackControl\n", controlHero.id, baseX, baseY)
					} else if attackMonster != nil {
						fmt.Printf("MOVE %d %d Attack\n", attackMonster.x, attackMonster.y)
					} else {
						if len(opHeroesSlice2) > 0 &&
							opHeroesSlice2[0].distanceToOpBase < 6000 {
							fmt.Printf("MOVE %d %d AttackFollowHero\n", opHeroesSlice2[0].x, opHeroesSlice2[0].y)
						} else {
							fmt.Printf("MOVE %d %d AttackPrepare\n", attackPosition.x, attackPosition.y)
						}
					}
				}
			}
		} else {
			for idx := 0; idx < heroesPerPlayer; idx++ {
				fmt.Printf("MOVE %d %d Prepare\n", preparePosition[idx].x, preparePosition[idx].y)
			}
		}
	}
}
