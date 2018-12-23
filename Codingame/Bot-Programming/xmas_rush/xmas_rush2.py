using System;
using System.Linq;
using System.IO;
using System.Text;
using System.Collections;
using System.Collections.Generic;

// TODO 2 items in save move
// item in player tile
// simulate

class Path
{
    public int cost;
    public List<Point> path;
    public Point next;
    public bool end {get; set;}
    public HashSet<Point> seen {get; set;}
    
    public Path(int cost, Point next, List<Point> path){
        this.cost = cost;
        this.next = next;
        this.path = path;
        this.end = false;
    }
    
    public override string ToString()
    {
        if(this.path.Count > 0)return String.Format("(cost:{0},this:{1},next:{2})",this.cost, this.path[this.path.Count-1], this.next);
        return String.Format("(cost:{0},next:{1})",this.cost, this.next);
    }
}

class Tile
{
    public String str {get; set;}
    
    public Tile(String s) {
        this.str = s;
    }
    
    public bool canUp() {
        return str[0] == '1';
    }
    
    public bool canRight() {
        return str[1] == '1';
    }
    
    public bool canDown() {
        return str[2] == '1';
    }
    
    public bool canLeft() {
        return str[3] == '1';
    }
}

class Map
{
    public Dictionary<Point, List<Point>> graph { get; set; }
    public Dictionary<Point, Tile> tiles { get; set; }
    public Dictionary<Point, Tile> backupTiles { get; set; }

    public Map(){
        this.tiles = new Dictionary<Point, Tile>();
    }
    
    public void add(Point p, Tile s) {
        tiles.Add(p, s);
    }
    
    public void pushRight(int id, Tile newTile) {
        for(int x=5; x>=0; x--)
        {
            tiles[new Point(x+1, id)] = tiles[new Point(x, id)];
        }
        tiles[new Point(0, id)] = newTile;
        
        this.buildGraph();
        foreach(Player p in Globals.players){
            if(p.y == id){
                p.moveRight();
            }
        }
        foreach(Item i in Globals.items){
            if(i.y == id){
                i.moveRight();
            }
            if(i.x == -1 && i.y == -1) {
                i.x = 0;
                i.y = id;
            }
        }
    }
    
    public void pushLeft(int id, Tile newTile) {
        for(int x=1; x<7; x++)
        {
            tiles[new Point(x-1, id)] = tiles[new Point(x, id)];
        }
        tiles[new Point(6, id)] = newTile;
        
        this.buildGraph();
        // Console.Error.WriteLine(String.Join(":", players[0].items));   
        foreach(Player p in Globals.players){
            if(p.y == id){
                p.moveLeft();
            }
        }
        foreach(Item i in Globals.items){
            if(i.y == id){
                i.moveLeft();
            }
            if(i.x == -1 && i.y == -1) {
                i.x = 6;
                i.y = id;
            }
        }
    }
    
    public void pushDown(int id, Tile newTile) {
        for(int y=5; y>=0; y--)
        {
            tiles[new Point(id, y+1)] = tiles[new Point(id, y)];
        }
        tiles[new Point(id, 0)] = newTile;
        
        this.buildGraph();
        foreach(Player p in Globals.players){
            if(p.x == id){
                p.moveDown();
            }
        }
        foreach(Item i in Globals.items){
            if(i.x == id){
                i.moveDown();
            }
            if(i.x == -1 && i.y == -1) {
                i.x = id;
                i.y = 0;
            }
        }
    }
    
    public void pushUp(int id, Tile newTile) {
        for(int y=1; y<7; y++)
        {
            tiles[new Point(id, y-1)] = tiles[new Point(id, y)];
        }
        tiles[new Point(id, 6)] = newTile;
        
        this.buildGraph();
        foreach(Player p in Globals.players){
            if(p.x == id){
                p.moveUp();
            }
        }
        foreach(Item i in Globals.items){
            if(i.x == id){
                i.moveUp();
            }
            if(i.x == -1 && i.y == -1) {
                i.x = id;
                i.y = 6;
            }
        }
    }
    
    public void buildGraph() {
        this.graph = new Dictionary<Point, List<Point>>();
        
        foreach(KeyValuePair<Point, Tile> tile in tiles)
        {
            List<Point> node = new List<Point>();
            if(tile.Key.y!=0 && tile.Value.canUp() && tiles[tile.Key.up()].canDown()) {
                node.Add(tile.Key.up());
            }
            if(tile.Key.x!=6 && tile.Value.canRight() && tiles[tile.Key.right()].canLeft()) {
                node.Add(tile.Key.right());
            }
            if(tile.Key.y!=6 &&tile.Value.canDown() && tiles[tile.Key.down()].canUp()) {
                node.Add(tile.Key.down());
            }
            if(tile.Key.x!=0 &&tile.Value.canLeft() && tiles[tile.Key.left()].canRight()) {
                node.Add(tile.Key.left());
            }
            graph.Add(tile.Key, node);       
        }
    }
    
    public void backup() {
        this.backupTiles = this.tiles.ToDictionary(entry => entry.Key, entry => entry.Value); // to deep copy
    }
    
    public void restore() {
        this.tiles = this.backupTiles.ToDictionary(entry => entry.Key, entry => entry.Value);
    }
}

class Point
{
    public int x { get; set; }
    public int y { get; set; }
    
    public int mod(int x, int m) {
        int r = x%m;
        return r<0 ? r+m : r;
    }
    
    public Point(int x, int y)
    {
        this.x = x;
        this.y = y;
    }
    
    public override bool Equals(Object obj) 
    {
        if (obj == null || GetType() != obj.GetType()) 
         return false;
        
        Point p = (Point)obj;
        return (this.x == p.x) && (this.y == p.y);
    }
    
    public int distance(int x, int y) { // ManhattanDistance
        return Math.Abs(this.x - x) + Math.Abs(this.y - y);
    }
    
    public override int GetHashCode() 
    {
        return  this.x ^ this.y;
    }
    
    public override string ToString()
    {
        return String.Format("({0},{1})",this.x, this.y);
    }
    
    public Point left() {
        return new Point(this.x-1, this.y);
    }
    
    public Point right() {
        return new Point(this.x+1, this.y);
    }
    
    public Point up() {
        return new Point(this.x, this.y-1);
    }
    
    public Point down() {
        return new Point(this.x, this.y+1);
    }
}

class Item: Point
{
    public String itemName {get; set;}
    public int itemPlayerId {get; set;} 
    
    public Item(int x, int y, String itemName, int itemPlayerId): base(x, y)
    {
        this.itemName = itemName;
        this.itemPlayerId = itemPlayerId;
    }
    
    public void moveLeft() {
        this.x = this.x-1;
        if(this.x < 0){
            this.x=-1;
            this.y=-1;
        }
    }
    
    public void moveRight() {
        this.x = this.x+1;
        if(this.x > 6){
            this.x=-1;
            this.y=-1;
        }
    }
    
    public void moveUp() {
        this.y = this.y-1;
        if(this.y < 0){
            this.x=-1;
            this.y=-1;
        }
    }
    
    public void moveDown() {
        this.y = this.y+1;
        if(this.y > 6){
            this.x=-1;
            this.y=-1;
        }
    }
}

class Player: Point
{
    public int numPlayerCards {get; set;}
    public Tile playerTile {get; set;}
    public List<Item> items {get; set;}
    public List<String> quests {get; set;}
    public List<Point> targets {get; set;}
    public Player opponent {get; set;}
    
    public int backupX {get; set;}
    public int backupY {get; set;}
    public List<Item> backupItems {get; set;}
    
    public Player(int x, int y, int numPlayerCards, Tile playerTile): base(x, y)
    {
        this.numPlayerCards = numPlayerCards;
        this.playerTile = playerTile;
        items = new List<Item>();
        quests = new List<String>();
    }
    
    public void removeItem() {
        this.items.RemoveAll(i => i.x == this.x && i.y == this.y);
        this.setTargetList();
    }
    
    public void moveLeft() {
        this.x = this.mod(this.x-1, 7);
    }
    
    public void moveRight() {
        this.x = this.mod(this.x+1, 7);
    }
    
    public void moveUp() {
        this.y = this.mod(this.y-1, 7);
    }
    
    public void moveDown() {
        this.y = this.mod(this.y+1, 7);
    }
    
    public void setTargetList() {
        targets = new List<Point>();
        for(int i=0; i<items.Count(); i++) {
            if(quests.Any(items[i].itemName.Contains)){
                targets.Add(new Point(items[i].x, items[i].y));
            }
        }
    }

    public int score(Dictionary<Point, List<Point>> graph) {
        return this.ShortestPathClosetItemCost(graph);
    }
    
    public int ShortestPathClosetItemCost(Dictionary<Point, List<Point>> graph){
        Path shortestPath = this.ShortestPathClosetItem(graph);
        if(shortestPath.end){
            return 0;
        }
        return 100;
    }
    
    public Path ShortestPathClosetItem(Dictionary<Point, List<Point>> graph){
        Queue<Path> queue = new Queue<Path>();
        queue.Enqueue(new Path(0, new Point(this.x, this.y), new List<Point>()));
        HashSet<Point> seen = new HashSet<Point>();
        while(queue.Count > 0){
            Path path_ = queue.Dequeue();
            if(!seen.Contains(path_.next)){
                List<Point> new_path = path_.path.ToList(); // use ToList to clone list<point>
                new_path.Add(path_.next);
                seen.Add(path_.next);
                if(this.targets.Contains(path_.next)){
                    path_.path = new_path;
                    return path_;
                }
                foreach(Point next in graph[path_.next]){
                    queue.Enqueue(new Path(path_.cost+1, next, new_path));
                }
            }
            if(queue.Count == 0){
                path_.end = true;
                path_.seen = seen;
                return path_;// return path_ if not see path
            }
        }
        return null;// return null if not see path
    }
    
    public string getDirectionMove(Point next_point) {
        if(next_point.x < this.backupX)return "LEFT";
        if(next_point.x > this.backupX)return "RIGHT";
        if(next_point.y < this.backupY)return "UP";
        if(next_point.y > this.backupY)return "DOWN";
        return null;
    }
    
    public void backup() {
        backupPos();
        backupItem();
    }
    
    public void restore() {
        restorePos();
        restoreItem();
    }
    
    public void backupPos() {
        this.backupX = this.x+0;
        this.backupY = this.y+0;
    }
    
    public void restorePos() {
        this.x = this.backupX+0;
        this.y = this.backupY+0;
    }
    
    public void backupItem() {
        this.backupItems = this.items.Select(i => new Item(i.x, i.y, i.itemName, i.itemPlayerId)).ToList();
    }
    
    public void restoreItem() {
        this.items = this.backupItems.Select(i => new Item(i.x, i.y, i.itemName, i.itemPlayerId)).ToList();
    }
}

class Push {
    public sealed static int up = 0;
    public sealed static int right = 1;
    public sealed static int down = 2;
    public sealed static int left = 3;
    
    public static string toString(int id, int direction) {
        if(direction == 0)return "PUSH "+id+" UP";
        if(direction == 1)return "PUSH "+id+" RIGHT";
        if(direction == 2)return "PUSH "+id+" DOWN";
        return "PUSH "+id+" LEFT";
    }
}

class Node
{
    public Node next {get; set;}
    public Node prev {get; set;}
    public int score {get; set;}
    public int turnType {get; set;}
    public string action {get; set;}
}

class Simulate
{
    List<Player> players;
    List<Item> items;
    Map map;
    int turnType;
    
    public Simulate() {
        this.players = Globals.players;
        this.items = Globals.items;
        this.map = Globals.map;
        this.turnType = Globals.turnType;
    }
    
    public string bestMove() {
        if(turnType == 0) {
            return push();
        } else {
            return move();
        }
    }
    
    string push() { // 28
        int bestScore = -999999999;
        int score;
        String bestAction = "";
        
        foreach(Player p in players) {
            p.backup();
        }
                
        for(int id=0; id<7; id++) { //id
            // LEFT
            map.restore();
            foreach(Player p in players){
                p.backup();
            }
            // Console.Error.WriteLine(map.tiles[new Point(0,0)].str);
            map.pushLeft(id, players[0].playerTile);
            // Console.Error.WriteLine(String.Join(":", players[0].items));   
            score = players[0].scorePush(map.graph);
            // Console.Error.WriteLine(id+";left;"+score);
            if(score > bestScore) {
                bestScore = score;
                bestAction = "PUSH "+id+" LEFT";
            }
            
            // RIGHT
            map.restore();
            foreach(Player p in players){
                p.restore();
            }
            map.pushRight(id, players[0].playerTile);
            score = players[0].scorePush(map.graph);
            // Console.Error.WriteLine(id+";right;"+score);
            if(score > bestScore) {
                bestScore = score;
                bestAction = "PUSH "+id+" RIGHT";
            }
            
            // UP
            map.restore();
            // Console.Error.WriteLine(map.tiles[new Point(4,5)].str);
            foreach(Player p in players){
                p.restore();
            }
            map.pushUp(id, players[0].playerTile);
            // Console.Error.WriteLine(map.tiles[new Point(4,5)].str);
            score = players[0].scorePush(map.graph);
            // Console.Error.WriteLine(id+";up;"+score);
            if(score > bestScore) {
                bestScore = score;
                bestAction = "PUSH "+id+" UP";
            }
            
            //Down
            map.restore();
            foreach(Player p in players){
                p.restore();
            }
            map.pushDown(id, players[0].playerTile);
            score = players[0].scorePush(map.graph);
            // Console.Error.WriteLine(id+";down;"+score);
            if(score > bestScore) {
                bestScore = score;
            }
        }
        if(bestScore != -999999999){
            return bestAction;
        }
        else{
            return "PUSH "+ 1 +" DOWN";
        }
    }
    
    string move() { // 4
        List<String> moves = new List<String>();
        map.buildGraph();
        
        Player me = players[0];
        
        int bestScore;
        int bestX;
        int bestY;
        int score;
        
        for(int i=0;i<20;i++){
            me.backupX = me.x+0;
            me.backupY = me.y+0;
            
            bestScore = me.scoreMove(map.graph);
            bestX = me.x;
            bestY = me.y;
            
            foreach (Point point in map.graph[new Point(me.x, me.y)]) {
                me.x = point.x;
                me.y = point.y;
                score = me.scoreMove(map.graph);
                if(score > bestScore) {
                    bestScore = score;
                    bestX = me.x;
                    bestY = me.y;
                }
            }
            if(bestX == me.backupX && bestY == me.backupY){
                break;
            }
            moves.Add(me.getDirectionMove(new Point(bestX, bestY)));
            me.x = bestX;
            me.y = bestY;
            me.removeItem();
        }
        if(moves.Count == 0){
            return "PASS";
        }
        return "MOVE "+String.Join(" ", moves.ToArray());
    }
}

class Globals
{
    public static List<Player> players;
    public static List<Item> items;
    public static Map map;
    public static int turnType;
    
    static void Main(string[] args)
    {
        string[] inputs;

        // game loop
        while (true)
        {
            map = new Map();            
            
            turnType = int.Parse(Console.ReadLine());
            for (int i = 0; i < 7; i++)
            {
                inputs = Console.ReadLine().Split(' ');
                for (int j = 0; j < 7; j++)
                {
                    string tile = inputs[j];
                    //Console.Error.WriteLine(tile);
                    map.add(new Point(j, i), new Tile(tile));
                }
            }
            
            players = new List<Player>();
            
            for (int i = 0; i < 2; i++)
            {
                inputs = Console.ReadLine().Split(' ');
                int numPlayerCards = int.Parse(inputs[0]); // the total number of quests for a player (hidden and revealed)
                int playerX = int.Parse(inputs[1]);
                int playerY = int.Parse(inputs[2]);
                string playerTile = inputs[3];
                
                players.Add(new Player(playerX, playerY, numPlayerCards, new Tile(playerTile)));
            }
            
            items = new List<Item>();
            
            int numItems = int.Parse(Console.ReadLine()); // the total number of items available on board and on player tiles
            for (int i = 0; i < numItems; i++)
            {
                inputs = Console.ReadLine().Split(' ');
                string itemName = inputs[0];
                int itemX = int.Parse(inputs[1]);
                int itemY = int.Parse(inputs[2]);
                int itemPlayerId = int.Parse(inputs[3]);
                
                items.Add(new Item(itemX, itemY, itemName, itemPlayerId));
                players[itemPlayerId].items.Add(items[i]);
            }
            
            int numQuests = int.Parse(Console.ReadLine()); // the total number of revealed quests for both players
            for (int i = 0; i < numQuests; i++)
            {
                inputs = Console.ReadLine().Split(' ');
                // Console.Error.WriteLine(inputs[0], inputs[1]);
                string questItemName = inputs[0];
                int questPlayerId = int.Parse(inputs[1]);
                players[questPlayerId].quests.Add(questItemName);
            }
            
            players[0].setTargetList();
            players[1].setTargetList();
            
            players[0].opponent = players[1];
            players[1].opponent = players[0];
            
            map.backup();
            
            Simulate sim = new Simulate();
            
            Console.WriteLine(sim.bestMove());
        }
    }
}
